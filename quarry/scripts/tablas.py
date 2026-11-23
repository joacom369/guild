"""Lectura de tablas para ficha.py y perfil.py: CSV, TSV, JSON, JSONL con la biblioteca estándar; XLSX y Parquet
si están instalados openpyxl o pandas.

Devuelve (columnas, filas): filas es una lista de diccionarios. Los valores de CSV llegan como texto, sin convertir.
"""
import csv
import json
from pathlib import Path

TABULARES = {".csv", ".tsv", ".txt", ".json", ".jsonl", ".ndjson", ".xlsx", ".xlsm", ".parquet"}


def _texto(ruta):
    for cod in ("utf-8-sig", "latin-1"):
        try:
            return ruta.read_text(encoding=cod)
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"No se pudo leer {ruta.name} como texto UTF-8 ni Latin-1.")


def _csv(ruta, sep=None):
    texto = _texto(ruta)
    if sep is None:
        if ruta.suffix == ".tsv":
            sep = "\t"
        else:
            try:
                sep = csv.Sniffer().sniff(texto[:20000], delimiters=",;\t|").delimiter
            except csv.Error:
                sep = ","
    lector = csv.DictReader(texto.splitlines(), delimiter=sep)
    filas = list(lector)
    return list(lector.fieldnames or []), filas


def _lista_de_registros(obj):
    """Busca la primera lista de diccionarios: la raíz o una clave como data, results, rows, items."""
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            if isinstance(v, list) and (not v or isinstance(v[0], dict)):
                return v
    raise SystemExit("El JSON no tiene una lista de registros.")


def _columnas(filas):
    cols = {}
    for f in filas:
        for k in f:
            cols.setdefault(k, None)
    return list(cols)


def _xlsx(ruta, hoja=None):
    try:
        import openpyxl
    except ImportError:
        raise SystemExit("Para leer .xlsx hace falta openpyxl: pip install openpyxl")
    libro = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    if hoja and hoja not in libro.sheetnames:
        raise SystemExit(f"No existe la hoja {hoja!r} en {ruta.name}. Hojas disponibles: {', '.join(libro.sheetnames)}")
    h = libro[hoja] if hoja else libro.worksheets[0]
    filas = h.iter_rows(values_only=True)
    encabezado = [str(c) if c is not None else f"col{i + 1}" for i, c in enumerate(next(filas, []))]
    datos = [dict(zip(encabezado, f)) for f in filas if any(c is not None for c in f)]
    return encabezado, datos


def _parquet(ruta):
    try:
        import pandas as pd
    except ImportError:
        raise SystemExit("Para leer .parquet hace falta pandas y pyarrow: pip install pandas pyarrow")
    try:
        df = pd.read_parquet(ruta)
    except ImportError:
        raise SystemExit("Para leer .parquet hace falta pyarrow o fastparquet: pip install pyarrow")
    return list(df.columns), df.astype(object).where(df.notna(), None).to_dict("records")


def leer(ruta, hoja=None, sep=None):
    ruta = Path(ruta)
    if not ruta.exists():
        raise SystemExit(f"No existe el archivo: {ruta}")
    if ruta.is_dir():
        raise SystemExit(f"{ruta} es una carpeta; pasá un archivo tabular.")
    ext = ruta.suffix.lower()
    if ext in (".csv", ".tsv", ".txt"):
        return _csv(ruta, sep)
    if ext == ".json":
        filas = _lista_de_registros(json.loads(_texto(ruta)))
        return _columnas(filas), filas
    if ext in (".jsonl", ".ndjson"):
        filas = [json.loads(l) for l in _texto(ruta).splitlines() if l.strip()]
        return _columnas(filas), filas
    if ext in (".xlsx", ".xlsm"):
        return _xlsx(ruta, hoja)
    if ext == ".parquet":
        return _parquet(ruta)
    raise SystemExit(f"No sé leer {ext}: convertilo a CSV o JSON.")
