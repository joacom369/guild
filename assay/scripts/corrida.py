"""Corre un análisis de forma reproducible y deja su ficha: entradas verificadas, comando, semilla, versión y salidas.

Uso:
    python corrida.py --nombre NOMBRE --entrada CARPETA_FOTO [--entrada OTRA] [--salidas salidas/] [--semilla 42] \
                      -- python analisis.py [argumentos]
    python corrida.py --verificar salidas/2026-10-25_101500_NOMBRE

Crea salidas/<fecha>_<hora>_<NOMBRE>/ (nunca pisa una corrida anterior) y corre el comando con estas variables:
    CORRIDA_DIR      carpeta donde el análisis tiene que escribir sus salidas
    CORRIDA_SEMILLA  semilla para todo lo aleatorio (también PYTHONHASHSEED)
Si una entrada tiene FICHA.json (de quarry), verifica sus hashes antes de correr y se detiene si algo cambió.
Al terminar escribe CORRIDA.json y log.txt. --verificar recalcula los hashes de las salidas y sale con 1 si cambiaron.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

FICHA, CORRIDA = "FICHA.json", "CORRIDA.json"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def verificar_entrada(carpeta):
    """Devuelve la descripción de la entrada; se detiene si su FICHA.json no coincide con los archivos."""
    carpeta = Path(carpeta)
    if not carpeta.exists():
        sys.exit(f"No existe la carpeta de entrada: {carpeta}")
    ficha = carpeta / FICHA
    if not ficha.exists():
        return {"carpeta": carpeta.as_posix(), "ficha": None, "nota": "sin FICHA.json: entrada no verificada"}
    datos = json.loads(ficha.read_text(encoding="utf-8"))
    malos = [d["archivo"] for d in datos["archivos"]
             if not (carpeta / d["archivo"]).exists() or sha256(carpeta / d["archivo"]) != d["sha256"]]
    if malos:
        sys.exit(f"La entrada {carpeta} no coincide con su ficha: {', '.join(malos)}. No se corre sobre datos cambiados.")
    return {"carpeta": carpeta.as_posix(), "ficha": sha256(ficha), "origen": datos.get("origen"),
            "extraido": datos.get("extraido"), "verificada": True}


def git_estado():
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        sucio = bool(subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip())
        return {"commit": commit, "cambios_sin_commit": sucio}
    except (OSError, subprocess.CalledProcessError):
        return None


def salidas_de(carpeta):
    return [{"archivo": p.relative_to(carpeta).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)}
            for p in sorted(carpeta.rglob("*")) if p.is_file() and p.name not in (CORRIDA, "log.txt")]


def correr(a, comando):
    entradas = [verificar_entrada(e) for e in a.entrada]
    inicio = datetime.now()
    carpeta = Path(a.salidas) / f"{inicio:%Y-%m-%d_%H%M%S}_{a.nombre}"
    carpeta.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, CORRIDA_DIR=str(carpeta.resolve()), CORRIDA_SEMILLA=str(a.semilla),
               PYTHONHASHSEED=str(a.semilla))
    t0 = time.time()
    try:
        with open(carpeta / "log.txt", "w", encoding="utf-8") as log:
            proc = subprocess.run(comando, env=env, stdout=log, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        shutil.rmtree(carpeta, ignore_errors=True)
        sys.exit(f"No se encontró el ejecutable {comando[0]!r}. Revisá el comando o el entorno virtual.")
    ficha = {
        "nombre": a.nombre, "comando": comando, "inicio": inicio.isoformat(timespec="seconds"),
        "duracion_s": round(time.time() - t0, 1), "codigo_salida": proc.returncode, "semilla": a.semilla,
        "python": sys.version.split()[0], "sistema": platform.platform(), "git": git_estado(),
        "entradas": entradas, "salidas": salidas_de(carpeta),
    }
    (carpeta / CORRIDA).write_text(json.dumps(ficha, ensure_ascii=False, indent=2), encoding="utf-8")
    estado = "OK" if proc.returncode == 0 else f"FALLÓ (código {proc.returncode}); ver log.txt"
    print(f"{estado}: {len(ficha['salidas'])} salidas en {carpeta}")
    sys.exit(proc.returncode)


def verificar(carpeta):
    carpeta = Path(carpeta)
    archivo = carpeta / CORRIDA
    if not archivo.exists():
        sys.exit(f"No hay {CORRIDA} en {carpeta}; verificá la ruta de la corrida.")
    ficha = json.loads(archivo.read_text(encoding="utf-8"))
    esperado = {d["archivo"]: d["sha256"] for d in ficha["salidas"]}
    actual = {d["archivo"]: d["sha256"] for d in salidas_de(carpeta)}
    problemas = [f"CAMBIÓ  {n}" for n in esperado if n in actual and actual[n] != esperado[n]]
    problemas += [f"FALTA   {n}" for n in esperado if n not in actual]
    problemas += [f"SOBRA   {n}" for n in actual if n not in esperado]
    if problemas:
        print("\n".join(problemas))
        sys.exit(1)
    print(f"OK: {len(esperado)} salidas iguales a la corrida del {ficha['inicio']}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    argv = sys.argv[1:]
    comando = argv[argv.index("--") + 1:] if "--" in argv else []
    argv = argv[:argv.index("--")] if "--" in argv else argv
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--verificar")
    p.add_argument("--nombre")
    p.add_argument("--entrada", action="append", default=[])
    p.add_argument("--salidas", default="salidas")
    p.add_argument("--semilla", type=int, default=42)
    a = p.parse_args(argv)
    if a.verificar:
        verificar(a.verificar)
    elif not (a.nombre and comando):
        p.error("hace falta --nombre y el comando después de --")
    else:
        correr(a, comando)
