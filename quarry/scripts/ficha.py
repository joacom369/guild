"""Escribe o verifica FICHA.json: la procedencia de una foto de datos.

Uso:
    python ficha.py CARPETA --origen "sistema.tabla" [--consulta archivo.sql|"texto"] [--periodo "2026-01..2026-09"]
                    [--herramienta "psql 16"] [--extraido 2026-10-25T10:00] [--nota "..."]
    python ficha.py CARPETA --verificar

La ficha guarda origen, consulta, período representado, fecha de extracción y, por archivo, bytes, SHA-256, filas
y columnas. No pisa una ficha existente: una corrida nueva va en otra carpeta. --verificar recalcula los hashes y
sale con código 1 si algún archivo cambió, falta o sobra.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # con «python -I» la carpeta del script no está en la ruta
from tablas import TABULARES, leer  # noqa: E402

FICHA = "FICHA.json"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def archivos(carpeta):
    return sorted(p for p in carpeta.rglob("*") if p.is_file() and p.name != FICHA)


def describir(carpeta, ruta):
    d = {"archivo": ruta.relative_to(carpeta).as_posix(), "bytes": ruta.stat().st_size, "sha256": sha256(ruta),
         "filas": None, "columnas": None}
    if ruta.suffix.lower() in TABULARES:
        try:
            cols, filas = leer(ruta)
            d["filas"], d["columnas"] = len(filas), cols
        except (SystemExit, Exception) as e:  # el archivo queda con su hash aunque no se pueda leer como tabla
            d["nota"] = f"no se leyó como tabla: {e}"
    return d


def escribir(a):
    carpeta = Path(a.carpeta)
    destino = carpeta / FICHA
    if destino.exists():
        sys.exit(f"Ya existe {destino}. Una corrida nueva va en otra carpeta; no se pisa la ficha.")
    consulta, consulta_archivo = a.consulta, None
    if a.consulta and Path(a.consulta).is_file():
        consulta_archivo = a.consulta
        consulta = Path(a.consulta).read_text(encoding="utf-8")
    ficha = {
        "origen": a.origen,
        "consulta": consulta,
        "consulta_archivo": consulta_archivo,
        "periodo_representado": a.periodo,
        "extraido": a.extraido or datetime.now().isoformat(timespec="seconds"),
        "herramienta": a.herramienta,
        "nota": a.nota,
        "archivos": [describir(carpeta, p) for p in archivos(carpeta)],
    }
    destino.write_text(json.dumps(ficha, ensure_ascii=False, indent=2), encoding="utf-8")
    for d in ficha["archivos"]:
        print(f"{d['archivo']}: {d['filas'] if d['filas'] is not None else '-'} filas, {d['sha256'][:12]}")
    print(f"Ficha escrita en {destino}")


def verificar(a):
    carpeta = Path(a.carpeta)
    ficha = json.loads((carpeta / FICHA).read_text(encoding="utf-8"))
    esperado = {d["archivo"]: d["sha256"] for d in ficha["archivos"]}
    actual = {p.relative_to(carpeta).as_posix(): p for p in archivos(carpeta)}
    problemas = []
    for nombre, h in esperado.items():
        if nombre not in actual:
            problemas.append(f"FALTA     {nombre}")
        elif sha256(actual[nombre]) != h:
            problemas.append(f"CAMBIÓ    {nombre}")
    problemas += [f"SOBRA     {n}" for n in actual if n not in esperado]
    if problemas:
        print("\n".join(problemas))
        sys.exit(1)
    print(f"OK: {len(esperado)} archivos iguales a la ficha del {ficha['extraido']}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("carpeta")
    p.add_argument("--verificar", action="store_true")
    p.add_argument("--origen")
    p.add_argument("--consulta")
    p.add_argument("--periodo")
    p.add_argument("--herramienta")
    p.add_argument("--extraido")
    p.add_argument("--nota")
    a = p.parse_args()
    if a.verificar:
        verificar(a)
    elif not a.origen:
        p.error("--origen es obligatorio al escribir la ficha")
    else:
        escribir(a)
