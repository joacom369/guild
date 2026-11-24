"""Arma dist/<skill>.zip para subir cada skill en claude.ai (Configuración > Capacidades > Skills).

Uso: python empaquetar.py [skill ...]        (sin argumentos: las skills propias y dist/SHA256SUMS)
     python empaquetar.py --piso skill       (sube el piso de disparo desde las corridas locales)
     python empaquetar.py --verificar-sha256 [DIR]  (compara archivos fuente contra dist/SHA256SUMS)
El ZIP lleva la carpeta de la skill en la raíz, como pide claude.ai.

Antes de empaquetar controla el piso de disparo de cada skill (<skill>/evals/piso.json). Las pruebas de disparo son
aleatorias, así que el piso guarda una tasa por caso, medida con 3 corridas o más, y no un «pasan todos». Bloquea si
la description o un caso cambiaron desde que se midió, si falta un caso del piso o si la corrida más nueva de un caso
(con 3 o más) queda más de un fallo por debajo de su tasa. Una corrida más chica sólo avisa. El piso sólo sube con
--piso; bajarlo es editar el archivo a mano y anotar el motivo en el mapa.
"""
import hashlib
import json
import sys
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).parent
PROPIAS = ["kiln", "provenance", "tokenwise", "compass", "quarry", "assay", "hallmark", "foundry", "sherpa", "foreman", "lenses", "herald"]
MINIMO = 3  # corridas por caso para medir o controlar una tasa
TEXTO_SHA = {".md", ".py", ".json", ".txt", ".sh", ".yml", ".yaml", ".html", ".css", ".js"}


def huella(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def huella_archivo(ruta):
    datos = ruta.read_bytes()
    if ruta.suffix.lower() in TEXTO_SHA:
        datos = datos.replace(b"\r\n", b"\n")
    return hashlib.sha256(datos).hexdigest()


def archivos_skill(carpeta):
    return sorted(f for f in carpeta.rglob("*") if f.is_file() and "__pycache__" not in f.parts and "evals" not in f.parts)


def validar_frontmatter(nombre, carpeta):
    """Valida el bloque YAML inicial de SKILL.md (con PyYAML si está instalado, más el corte de ': ')."""
    texto = (carpeta / "SKILL.md").read_text(encoding="utf-8")
    fin = texto.find("\n---", 3)
    assert texto.startswith("---") and fin >= 0, f"{nombre}: falta frontmatter YAML válido (---)"
    crudo = texto[3:fin]
    # «: » dentro de una description sin comillas rompe el YAML y la skill se anuncia sin description;
    # claude plugin validate no lo detecta.
    for linea in crudo.splitlines():
        clave, _, valor = linea.partition(": ")
        roto = clave == "description" and valor[:1] not in "\"'>|" and ": " in valor
        assert not roto, f"{nombre}: la description tiene «: » sin comillas; cambialo por «; » o «,»"
    try:
        import yaml
    except ImportError:
        return
    try:
        datos = yaml.safe_load(crudo)
    except yaml.YAMLError as e:
        raise SystemExit(f"{nombre}: YAML inválido en frontmatter: {e}")
    assert isinstance(datos, dict), f"{nombre}: el frontmatter YAML no es un diccionario"
    assert isinstance(datos.get("description"), str) and datos["description"].strip(), (
        f"{nombre}: falta una 'description' de texto en el frontmatter"
    )


def escribir_sha256sums(nombres):
    destino = RAIZ / "dist" / "SHA256SUMS"
    destino.parent.mkdir(exist_ok=True)
    lineas = ["# SHA-256 de archivos fuente (texto normalizado a LF para paridad Windows/Linux)\n"]
    for nombre in sorted(nombres):
        carpeta = RAIZ / nombre
        for f in archivos_skill(carpeta):
            lineas.append(f"{huella_archivo(f)}  {f.relative_to(RAIZ).as_posix()}\n")
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("".join(lineas))
    print(f"{destino.relative_to(RAIZ).as_posix()}: {len(lineas) - 1} archivos fuente")


def verificar_sha256(raiz_destino=None):
    manifiesto = RAIZ / "dist" / "SHA256SUMS"
    if not manifiesto.exists():
        sys.exit(f"No existe {manifiesto}. Corré primero `python empaquetar.py`.")
    objetivo = Path(raiz_destino) if raiz_destino else RAIZ
    if not objetivo.is_dir():
        sys.exit(f"No existe la carpeta a verificar: {objetivo}")
    esperados = []
    for linea in manifiesto.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        digest, _, rel = linea.partition("  ")
        if not digest or not rel:
            sys.exit(f"Línea inválida en {manifiesto.name}: {linea}")
        esperados.append((digest, rel))
    problemas = []
    for digest, rel in esperados:
        ruta = objetivo / rel
        if not ruta.exists():
            problemas.append(f"FALTA   {rel}")
        elif huella_archivo(ruta) != digest:
            problemas.append(f"CAMBIÓ  {rel}")
    if problemas:
        print("\n".join(problemas))
        sys.exit(1)
    print(f"OK: {len(esperados)} archivos fuente coinciden con dist/SHA256SUMS")


def description(carpeta):
    """El texto crudo de la description en el frontmatter, con sus líneas de continuación."""
    lineas, dentro = [], False
    for linea in (carpeta / "SKILL.md").read_text(encoding="utf-8").split("---")[1].splitlines():
        if linea.startswith("description:"):
            dentro = True
        elif dentro and linea[:1] not in " \t":
            break
        if dentro:
            lineas.append(linea)
    return "\n".join(lineas)


def pedido(carpeta, caso):
    """El texto del caso sin su frontmatter: es lo que la corrida guarda como promptMarkdown."""
    return (carpeta / "evals" / caso / "prompt.md").read_text(encoding="utf-8").split("---", 2)[2].strip()


def casos_actuales(carpeta):
    return sorted(p.parent.name for p in (carpeta / "evals").glob("*/prompt.md"))


def corridas(carpeta, modelo, desde=""):
    """{caso: [(fecha, pasadas, total)]} de las corridas completas con ese modelo, sólo de la versión actual de cada caso."""
    textos = {c: pedido(carpeta, c) for c in casos_actuales(carpeta)}
    hallado = {}
    for f in sorted((carpeta / "evals" / "results").glob("*/aggregate-result.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        if j.get("partial") or j["suite"].get("modelOverride") != modelo or j["startedAt"] < desde:
            continue
        for c in j["cases"]:
            if textos.get(c["name"]) == c["promptMarkdown"].strip():
                vueltas = c["arms"]["with"]
                hallado.setdefault(c["name"], []).append((j["startedAt"], sum(v["passed"] for v in vueltas), len(vueltas)))
    return hallado


def controlar_piso(nombre, carpeta):
    """Devuelve (errores, avisos, resumen)."""
    archivo = carpeta / "evals" / "piso.json"
    if not archivo.exists():
        return [f"no tiene evals/piso.json; corré sus pruebas de disparo y `--piso {nombre}`"], [], ""
    piso = json.loads(archivo.read_text(encoding="utf-8"))
    errores, avisos = [], []
    if huella(description(carpeta)) != piso["description_sha256"]:
        errores.append(f"la description cambió desde que se midió; corré sus pruebas de disparo y `--piso {nombre}`")
    hallado = corridas(carpeta, piso["modelo"])
    for caso, medido in piso["casos"].items():
        if not (carpeta / "evals" / caso / "prompt.md").exists():
            errores.append(f"falta el caso {caso} del piso")
            continue
        if huella(pedido(carpeta, caso)) != medido["sha256"]:
            errores.append(f"el caso {caso} cambió desde que se midió; corrélo y `--piso {nombre}`")
            continue
        if caso not in hallado:
            continue
        _, pasadas, total = hallado[caso][-1]
        if total >= MINIMO and pasadas < medido["tasa"] * total - 1:
            errores.append(f"{caso}: {pasadas}/{total} en su corrida más nueva, piso {medido['tasa']:.0%}")
        elif total < MINIMO and pasadas < total:
            avisos.append(f"{caso}: {pasadas}/{total} con menos de {MINIMO} corridas (no bloquea)")
    nuevos = set(casos_actuales(carpeta)) - set(piso["casos"])
    if nuevos:
        avisos.append(f"casos fuera del piso: {', '.join(sorted(nuevos))}")
    tasas = ", ".join(f"{c} {m['tasa']:.0%}" for c, m in piso["casos"].items() if m["tasa"] < 1)
    resumen = f"{len(piso['casos'])} casos" + (f" (bajo 100%: {tasas})" if tasas else "")
    if not hallado:
        resumen += ", sin corridas en esta PC (no se controló el resultado)"
    return errores, avisos, resumen


def subir_piso(nombre, modelo="sonnet"):
    """Mide la tasa de cada caso con las corridas posteriores al último cambio del SKILL.md y sube el piso."""
    carpeta = RAIZ / nombre
    archivo = carpeta / "evals" / "piso.json"
    cambio = datetime.fromtimestamp((carpeta / "SKILL.md").stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    hallado = corridas(carpeta, modelo, desde=cambio)
    viejo = json.loads(archivo.read_text(encoding="utf-8"))["casos"] if archivo.exists() else {}
    casos, faltan = {}, []
    for caso in casos_actuales(carpeta):
        pasadas = sum(p for _, p, _ in hallado.get(caso, []))
        total = sum(t for _, _, t in hallado.get(caso, []))
        if total < MINIMO:
            faltan.append(f"{caso} ({total})")
            continue
        sha = huella(pedido(carpeta, caso))
        tasa = round(pasadas / total, 2)
        if caso in viejo and viejo[caso]["sha256"] == sha:
            tasa = max(tasa, viejo[caso]["tasa"])
        casos[caso] = {"tasa": tasa, "corridas": total, "sha256": sha}
    assert not faltan, (f"{nombre}: menos de {MINIMO} corridas con {modelo} desde el último cambio del SKILL.md "
                        f"({cambio}): {', '.join(faltan)}")
    perdidos = set(viejo) - set(casos)
    assert not perdidos, f"{nombre}: el piso bajaría (faltan {', '.join(perdidos)}); se baja a mano, con motivo"
    archivo.write_text(json.dumps({
        "modelo": modelo,
        "fecha": date.today().isoformat(),
        "description_sha256": huella(description(carpeta)),
        "casos": casos,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{archivo.relative_to(RAIZ)}: " + ", ".join(f"{c} {m['tasa']:.0%} ({m['corridas']})" for c, m in casos.items()))


if sys.argv[1:2] == ["--piso"]:
    for nombre in sys.argv[2:]:
        subir_piso(nombre)
    sys.exit()

if sys.argv[1:2] == ["--verificar-sha256"]:
    verificar_sha256(sys.argv[2] if len(sys.argv) > 2 else None)
    sys.exit()

objetivos = sys.argv[1:] or PROPIAS
bloqueadas = []
for nombre in objetivos:
    carpeta = RAIZ / nombre
    assert (carpeta / "SKILL.md").exists(), f"{nombre}: no tiene SKILL.md"
    validar_frontmatter(nombre, carpeta)
    errores, avisos, resumen = controlar_piso(nombre, carpeta)
    for aviso in avisos:
        print(f"  aviso {nombre}: {aviso}")
    if errores:
        bloqueadas.append(nombre)
        for error in errores:
            print(f"  NO SALE {nombre}: {error}")
        continue
    destino = RAIZ / "dist" / f"{nombre}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in archivos_skill(carpeta):
            z.write(f, f.relative_to(RAIZ).as_posix())
    print(f"{destino.relative_to(RAIZ)}: {destino.stat().st_size // 1024} KB; disparo: {resumen}")

if bloqueadas:
    sys.exit(f"No se empaquetaron: {', '.join(bloqueadas)}")

if not sys.argv[1:]:
    escribir_sha256sums(objetivos)
