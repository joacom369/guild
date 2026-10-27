"""Arma dist/<skill>.zip para subir cada skill en claude.ai (Configuración > Capacidades > Skills).

Uso: python empaquetar.py [skill ...]   (sin argumentos: las skills propias)
     python empaquetar.py --piso skill  (sube el piso de disparo desde las corridas locales)
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


def huella(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


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

bloqueadas = []
for nombre in sys.argv[1:] or PROPIAS:
    carpeta = RAIZ / nombre
    assert (carpeta / "SKILL.md").exists(), f"{nombre}: no tiene SKILL.md"
    # «: » dentro de una description sin comillas rompe el YAML y la skill se anuncia sin description;
    # claude plugin validate no lo detecta.
    for linea in (carpeta / "SKILL.md").read_text(encoding="utf-8").split("---")[1].splitlines():
        clave, _, valor = linea.partition(": ")
        roto = clave == "description" and valor[:1] not in "\"'>|" and ": " in valor
        assert not roto, f"{nombre}: la description tiene «: » sin comillas; cambialo por «; » o «,»"
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
        for f in sorted(carpeta.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and "evals" not in f.parts:
                z.write(f, f.relative_to(RAIZ).as_posix())
    print(f"{destino.relative_to(RAIZ)}: {destino.stat().st_size // 1024} KB; disparo: {resumen}")

if bloqueadas:
    sys.exit(f"No se empaquetaron: {', '.join(bloqueadas)}")
