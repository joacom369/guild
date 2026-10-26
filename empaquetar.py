"""Arma dist/<skill>.zip para subir cada skill en claude.ai (Configuración > Capacidades > Skills).

Uso: python empaquetar.py [skill ...]   (sin argumentos: las skills propias)
El ZIP lleva la carpeta de la skill en la raíz, como pide claude.ai.
"""
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).parent
PROPIAS = ["kiln", "provenance", "tokenwise", "compass", "quarry", "assay", "hallmark", "foundry", "sherpa", "foreman", "lenses", "herald"]

for nombre in sys.argv[1:] or PROPIAS:
    carpeta = RAIZ / nombre
    assert (carpeta / "SKILL.md").exists(), f"{nombre}: no tiene SKILL.md"
    # «: » dentro de una description sin comillas rompe el YAML y la skill se anuncia sin description;
    # claude plugin validate no lo detecta.
    for linea in (carpeta / "SKILL.md").read_text(encoding="utf-8").split("---")[1].splitlines():
        clave, _, valor = linea.partition(": ")
        roto = clave == "description" and valor[:1] not in "\"'>|" and ": " in valor
        assert not roto, f"{nombre}: la description tiene «: » sin comillas; cambialo por «; » o «,»"
    destino = RAIZ / "dist" / f"{nombre}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(carpeta.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and "evals" not in f.parts:
                z.write(f, f.relative_to(RAIZ).as_posix())
    print(f"{destino.relative_to(RAIZ)}: {destino.stat().st_size // 1024} KB")
