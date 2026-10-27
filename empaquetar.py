"""Arma dist/<skill>.zip para subir cada skill en claude.ai (Configuración > Capacidades > Skills).

Uso: python empaquetar.py [skill ...]   (sin argumentos: las skills propias)
     python empaquetar.py --piso skill  (sube el piso de disparo desde las corridas locales)
El ZIP lleva la carpeta de la skill en la raíz, como pide claude.ai.

Antes de empaquetar controla el piso de disparo de cada skill (<skill>/evals/piso.json): la description es la que
se probó, los casos del piso siguen existiendo y, si hay corridas en esta PC, ninguno falla en su corrida más nueva.
El piso sólo sube con --piso; bajarlo es editar el archivo a mano y anotar el motivo.
"""
import hashlib
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).parent
PROPIAS = ["kiln", "provenance", "tokenwise", "compass", "quarry", "assay", "hallmark", "foundry", "sherpa", "foreman", "lenses", "herald"]


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


def ultimo_por_caso(carpeta, modelo):
    """{caso: (fecha, pasó)} con la corrida más nueva de cada caso, sólo corridas completas con ese modelo."""
    casos = {}
    for f in sorted((carpeta / "evals" / "results").glob("*/aggregate-result.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        if j.get("partial") or j["suite"].get("modelOverride") != modelo:
            continue
        for c in j["cases"]:
            casos[c["name"]] = (j["startedAt"], c["aggregates"]["passRate"] == 1)
    return casos


def controlar_piso(nombre, carpeta):
    archivo = carpeta / "evals" / "piso.json"
    assert archivo.exists(), f"{nombre}: no tiene evals/piso.json; corré sus pruebas de disparo y `--piso {nombre}`"
    piso = json.loads(archivo.read_text(encoding="utf-8"))
    sha = hashlib.sha256(description(carpeta).encode("utf-8")).hexdigest()
    assert sha == piso["description_sha256"], (
        f"{nombre}: la description cambió desde que se probó; corré sus pruebas de disparo y `--piso {nombre}`")
    for caso in piso["casos"]:
        assert (carpeta / "evals" / caso / "prompt.md").exists(), f"{nombre}: falta el caso {caso} del piso"
    corridas = ultimo_por_caso(carpeta, piso["modelo"])
    if not corridas:
        return f"{len(piso['casos'])} casos, sin corridas en esta PC (no se controló el resultado)"
    fallan = [c for c in piso["casos"] if c in corridas and not corridas[c][1]]
    assert not fallan, f"{nombre}: fallan casos del piso en su corrida más nueva: {', '.join(fallan)}"
    return f"{len(piso['casos'])} casos, todos pasan"


def subir_piso(nombre, modelo="sonnet"):
    carpeta = RAIZ / nombre
    archivo = carpeta / "evals" / "piso.json"
    casos = sorted(p.parent.name for p in (carpeta / "evals").glob("*/prompt.md"))
    corridas = ultimo_por_caso(carpeta, modelo)
    faltan = [c for c in casos if c not in corridas or not corridas[c][1]]
    assert not faltan, f"{nombre}: sin corrida o sin pasar con {modelo}: {', '.join(faltan)}"
    if archivo.exists():
        perdidos = set(json.loads(archivo.read_text(encoding="utf-8"))["casos"]) - set(casos)
        assert not perdidos, f"{nombre}: el piso bajaría (faltan {', '.join(perdidos)}); se baja a mano, con motivo"
    archivo.write_text(json.dumps({
        "modelo": modelo,
        "fecha": date.today().isoformat(),
        "ultima_corrida": max(corridas[c][0] for c in casos),
        "description_sha256": hashlib.sha256(description(carpeta).encode("utf-8")).hexdigest(),
        "casos": casos,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{archivo.relative_to(RAIZ)}: {len(casos)} casos")


if sys.argv[1:2] == ["--piso"]:
    for nombre in sys.argv[2:]:
        subir_piso(nombre)
    sys.exit()

for nombre in sys.argv[1:] or PROPIAS:
    carpeta = RAIZ / nombre
    assert (carpeta / "SKILL.md").exists(), f"{nombre}: no tiene SKILL.md"
    # «: » dentro de una description sin comillas rompe el YAML y la skill se anuncia sin description;
    # claude plugin validate no lo detecta.
    for linea in (carpeta / "SKILL.md").read_text(encoding="utf-8").split("---")[1].splitlines():
        clave, _, valor = linea.partition(": ")
        roto = clave == "description" and valor[:1] not in "\"'>|" and ": " in valor
        assert not roto, f"{nombre}: la description tiene «: » sin comillas; cambialo por «; » o «,»"
    estado_piso = controlar_piso(nombre, carpeta)
    destino = RAIZ / "dist" / f"{nombre}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(carpeta.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and "evals" not in f.parts:
                z.write(f, f.relative_to(RAIZ).as_posix())
    print(f"{destino.relative_to(RAIZ)}: {destino.stat().st_size // 1024} KB; disparo: {estado_piso}")
