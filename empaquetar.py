"""Arma dist/<skill>.zip para subir cada skill en claude.ai (Configuración > Capacidades > Skills).

Uso: python empaquetar.py [skill ...]   (sin argumentos: las skills propias)
El ZIP lleva la carpeta de la skill en la raíz, como pide claude.ai.
"""
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).parent
PROPIAS = ["kiln", "provenance", "tokenwise"]

for nombre in sys.argv[1:] or PROPIAS:
    carpeta = RAIZ / nombre
    assert (carpeta / "SKILL.md").exists(), f"{nombre}: no tiene SKILL.md"
    destino = RAIZ / "dist" / f"{nombre}.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(carpeta.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(RAIZ).as_posix())
    print(f"{destino.relative_to(RAIZ)}: {destino.stat().st_size // 1024} KB")
