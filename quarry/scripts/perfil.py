"""Perfil de una tabla al llegar: vacíos separados de ceros, distintos, rangos, clave y cardinalidad de un cruce.

Uso:
    python perfil.py ARCHIVO [--hoja NOMBRE] [--sep ";"] [--decimal ,] [--clave col1,col2]
                     [--cruzar OTRO --por col | --por col_aca=col_alla]

Formatos: CSV, TSV, JSON, JSONL (biblioteca estándar); XLSX con openpyxl; Parquet con pandas.
--decimal fija el separador decimal de los textos ("." por defecto). No se adivina: con "," se lee 1.234,5. Un
valor que no encaja con el separador no se convierte: la columna queda como texto y el perfil sugiere el otro.
Vacío es una celda sin valor o con una marca de faltante (NULL, NA, #N/A...); cada marca se cuenta aparte.
Un cero es un valor numérico igual a cero. Son cosas distintas y se informan separadas.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # con «python -I» la carpeta del script no está en la ruta
from tablas import leer  # noqa: E402

MARCAS_VACIO = {"", "na", "n/a", "null", "none", "nan", "#n/a", "nil", "sin dato", "s/d"}
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?.*)?$")


def numero(v, decimal):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip().replace(" ", "")
    miles = "." if decimal == "," else ","
    entero, _, frac = s.partition(decimal)
    signo = -1 if entero.startswith("-") else 1
    entero = entero.lstrip("+-")
    if miles in entero:  # sólo grupos de tres: «1.234,50» con decimal «.» no se lee como 1,2345
        grupos = entero.split(miles)
        if not (1 <= len(grupos[0]) <= 3 and all(len(g) == 3 for g in grupos[1:])):
            return None
        entero = "".join(grupos)
    if not entero.isdigit() or (frac and not frac.isdigit()):
        return None
    return signo * float(f"{entero}.{frac or 0}")


def corto(n):
    return int(n) if float(n).is_integer() else n


def marca_vacio(v):
    """Devuelve la marca de vacío ('(en blanco)', 'NULL'...) o None si la celda tiene valor."""
    if v is None:
        return "(sin valor)"
    if isinstance(v, str) and v.strip().lower() in MARCAS_VACIO:
        return v.strip() or "(en blanco)"
    return None


def perfil_columna(nombre, valores, decimal):
    vacios = Counter(m for m in map(marca_vacio, valores) if m)
    llenos = [v for v in valores if marca_vacio(v) is None]
    nums = [numero(v, decimal) for v in llenos]
    es_num = bool(llenos) and all(n is not None for n in nums)
    es_fecha = bool(llenos) and not es_num and all(FECHA.match(str(v)) for v in llenos)
    distintos = Counter(map(str, llenos))
    if es_num:
        tipo, minimo, maximo = "número", corto(min(nums)), corto(max(nums))
        ceros = sum(1 for n in nums if n == 0)
    elif es_fecha:
        tipo, minimo, maximo, ceros = "fecha", min(map(str, llenos)), max(map(str, llenos)), 0
    else:
        parcial = sum(n is not None for n in nums)
        otro = "," if decimal == "." else "."
        if all(numero(v, otro) is not None for v in llenos):
            tipo = f"texto (¿decimal «{otro}»? probá --decimal {otro})"
        else:
            tipo = f"texto ({parcial} parecen número)" if parcial else "texto"
        minimo = maximo = ""
        ceros = sum(1 for n in nums if n == 0)
    vac = sum(vacios.values())
    detalle = ", ".join(f"{k}: {c}" for k, c in vacios.most_common())
    ejemplos = ", ".join(k for k, _ in distintos.most_common(3))
    return [nombre, tipo, len(llenos), f"{vac}" + (f" ({detalle})" if detalle else ""), ceros, len(distintos),
            minimo, maximo, ejemplos]


def tabla_md(encabezado, filas):
    lineas = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    for f in filas:
        lineas.append("| " + " | ".join(str(c).replace("|", "/")[:40] for c in f) + " |")
    return "\n".join(lineas)


def valor_clave(fila, cols):
    vals = [fila.get(c) for c in cols]
    if any(marca_vacio(v) for v in vals):
        return None
    return tuple(str(corto(v) if isinstance(v, float) else v).strip() for v in vals)  # 10.0 de Excel = "10"


def revisar_clave(filas, cols):
    claves = [valor_clave(f, cols) for f in filas]
    sin = claves.count(None)
    cuenta = Counter(k for k in claves if k is not None)
    repetidas = {k: c for k, c in cuenta.items() if c > 1}
    filas_rep = sum(repetidas.values())
    print(f"\n## Clave ({', '.join(cols)})\n")
    print(f"- Filas: {len(filas)} · con clave vacía: {sin} · claves distintas: {len(cuenta)}")
    if repetidas:
        ej = ", ".join(f"{'/'.join(k)} ×{c}" for k, c in list(repetidas.items())[:5])
        print(f"- **No es única:** {len(repetidas)} valores repetidos en {filas_rep} filas. Ejemplos: {ej}")
    else:
        print("- Única entre las filas con clave.")


def revisar_cruce(filas, otro, por, hoja, sep):
    aca, _, alla = por.partition("=")
    alla = alla or aca
    _, filas_otro = leer(otro, hoja, sep)
    indice = Counter(valor_clave(f, [alla]) for f in filas_otro)
    indice.pop(None, None)
    sin_clave = ninguna = una = varias = 0
    usadas = set()
    for f in filas:
        k = valor_clave(f, [aca])
        if k is None:
            sin_clave += 1
            continue
        n = indice.get(k, 0)
        usadas.add(k)
        if n == 0:
            ninguna += 1
        elif n == 1:
            una += 1
        else:
            varias += 1
    total = len(filas)
    huerfanas = sum(c for k, c in indice.items() if k not in usadas)
    print(f"\n## Cruce `{aca}` → {Path(otro).name} `{alla}`\n")
    print(tabla_md(["Resultado", "Filas", "%"], [
        ["exactamente una pareja", una, f"{100 * una / total:.1f}" if total else "-"],
        ["ninguna pareja", ninguna, f"{100 * ninguna / total:.1f}" if total else "-"],
        ["más de una pareja (ambiguo)", varias, f"{100 * varias / total:.1f}" if total else "-"],
        ["clave vacía", sin_clave, f"{100 * sin_clave / total:.1f}" if total else "-"],
        ["**total**", una + ninguna + varias + sin_clave, ""],
    ]))
    assert una + ninguna + varias + sin_clave == total
    print(f"\nDel otro lado: {len(filas_otro)} filas, {huerfanas} sin pareja de este lado.")
    if varias:
        print("Hay filas con más de una pareja: el cruce no es 1:1 y multiplica filas si se une sin más.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("archivo")
    p.add_argument("--hoja")
    p.add_argument("--sep")
    p.add_argument("--decimal", choices=[".", ","], default=".")
    p.add_argument("--clave")
    p.add_argument("--cruzar")
    p.add_argument("--por")
    a = p.parse_args()
    if bool(a.cruzar) != bool(a.por):
        p.error("--cruzar y --por van juntos")

    cols, filas = leer(a.archivo, a.hoja, a.sep)
    print(f"# Perfil de {Path(a.archivo).name}\n")
    print(f"{len(filas)} filas · {len(cols)} columnas · decimal «{a.decimal}»\n")
    print(tabla_md(["Columna", "Tipo", "Con valor", "Vacíos", "Ceros", "Distintos", "Mín", "Máx", "Más frecuentes"],
                   [perfil_columna(c, [f.get(c) for f in filas], a.decimal) for c in cols]))
    if a.clave:
        revisar_clave(filas, [c.strip() for c in a.clave.split(",")])
    if a.cruzar:
        revisar_cruce(filas, a.cruzar, a.por, a.hoja, a.sep)
