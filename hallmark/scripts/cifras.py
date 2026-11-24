"""Busca cada cifra de un entregable en las salidas del cálculo y lista las que no aparecen (huérfanas).

Uso:
    python cifras.py ENTREGABLE [ENTREGABLE ...] --fuentes SALIDA [SALIDA ...] --decimal ,
                     [--decimal-fuentes .] [--escala 1000 --escala 1e6] [--ignorar REGEX ...] [--todas]

Entregable: .md, .txt, .html, .docx, .xlsx, .csv, .json, .tex (sin comentarios %), .pdf (requiere pypdf,
PyMuPDF o pdftotext). Fuentes: archivos o carpetas con las salidas (CSV, JSON, logs, texto, .xlsx). Se recorren
las carpetas.

--decimal es el separador decimal del entregable y es obligatorio: «1.234» es mil doscientos treinta y cuatro con
«,» y uno coma dos con «.». No se adivina. --decimal-fuentes es el de las salidas («.» por defecto).
--ignorar excluye coincidencias de una expresión regular en el entregable (p. ej. normas o secciones).

Una cifra coincide si algún valor de las fuentes, redondeado a los decimales que muestra el entregable, da esa cifra:
«0,59» coincide con 0.587; «0,52» no. Un porcentaje también se compara como fracción (45 % ↔ 0.45). Los sufijos
(mil, M, MM) no se escalan solos: --escala 1000 hace que «12,3» pueda coincidir con 12 300.

Grupos: encontradas · huérfanas (no hay valor compatible en las fuentes) · ambiguas (el formato no encaja con el
separador declarado) · triviales (años y enteros de un dígito; se listan, no se verifican).
Sale con código 1 si hay huérfanas o ambiguas.

Límite: «encontrada» quiere decir que existe un valor compatible en las fuentes, no que sea el que corresponde.
Una cifra corta (12, 3,5) coincide con facilidad; por eso se informa en cuántos lugares aparece.
"""
import argparse
import bisect
import csv
import json
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

LEIBLES = {".md", ".txt", ".csv", ".tsv", ".json", ".jsonl", ".log", ".html", ".htm", ".xml", ".sql", ".py", ".r",
           ".docx", ".xlsx", ".xlsm", ".yaml", ".yml", ".tex", ".pdf"}
FECHAS = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b")
NUMERO = re.compile(r"(?<![\w.,])[-−+]?\d[\d.,]*(?:\s?%)?(?![\w])")


class _Texto(HTMLParser):
    def __init__(self):
        super().__init__()
        self.partes, self._saltar = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._saltar += 1
        elif tag in ("p", "div", "tr", "li", "br", "h1", "h2", "h3", "h4", "td", "th"):
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._saltar -= 1

    def handle_data(self, data):
        if not self._saltar:
            self.partes.append(data)


def texto_de(ruta):
    ext = ruta.suffix.lower()
    if ext in (".html", ".htm"):
        p = _Texto()
        p.feed(ruta.read_text(encoding="utf-8", errors="replace"))
        return "".join(p.partes)
    if ext == ".docx":
        xml = zipfile.ZipFile(ruta).read("word/document.xml").decode("utf-8")
        xml = re.sub(r"</w:p>", "\n", xml)
        return re.sub(r"<[^>]+>", "", xml)
    if ext == ".tex":
        texto = ruta.read_text(encoding="utf-8", errors="replace")
        texto = re.sub(r"(?<!\\)((?:\\\\)*)%.*$", r"\1", texto, flags=re.M)
        return texto.replace(r"\%", "%")
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(str(ruta)).pages)
        except ImportError:
            pass
        try:
            import fitz
            with fitz.open(str(ruta)) as doc:
                return "\n".join(page.get_text() for page in doc)
        except ImportError:
            pass
        if shutil.which("pdftotext"):
            try:
                return subprocess.run(
                    ["pdftotext", str(ruta), "-"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", check=True
                ).stdout
            except subprocess.CalledProcessError as e:
                raise SystemExit(f"No se pudo leer {ruta.name} con pdftotext: {e}")
        raise SystemExit("Para leer .pdf hace falta pypdf (pip install pypdf), PyMuPDF o pdftotext")
    return ruta.read_text(encoding="utf-8", errors="replace")


ESTRUCTURADOS = {".xlsx", ".xlsm", ".csv", ".tsv", ".json", ".jsonl"}


def celdas(ruta):
    """Itera (lugar, valor) de un archivo estructurado: celdas de una hoja, campos de un CSV, hojas de un JSON."""
    ext = ruta.suffix.lower()
    if ext in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            raise SystemExit("Para leer .xlsx hace falta openpyxl: pip install openpyxl")
        libro = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        for h in libro.worksheets:
            for n, fila in enumerate(h.iter_rows(values_only=True), 1):
                for c in fila:
                    yield f"{h.title}!{n}", c
    elif ext in (".csv", ".tsv"):
        texto = ruta.read_text(encoding="utf-8-sig", errors="replace")
        try:
            sep = csv.Sniffer().sniff(texto[:20000], delimiters=",;\t|").delimiter
        except csv.Error:
            sep = "\t" if ext == ".tsv" else ","
        for n, fila in enumerate(csv.reader(texto.splitlines(), delimiter=sep), 1):
            for c in fila:
                yield n, c
    else:
        texto = ruta.read_text(encoding="utf-8-sig")
        docs = [json.loads(texto)] if ext == ".json" else [json.loads(l) for l in texto.splitlines() if l.strip()]
        pila = [(i + 1, d) for i, d in enumerate(docs)]
        while pila:
            n, o = pila.pop()
            if isinstance(o, dict):
                pila += [(n, v) for v in o.values()]
            elif isinstance(o, list):
                pila += [(n, v) for v in o]
            else:
                yield n, o


def nativo(v):
    """Un número que ya es número se toma tal cual, sin volver a leerlo como texto."""
    texto = repr(v)
    frac = texto.partition(".")[2] if isinstance(v, float) and "e" not in texto else ""
    return float(v), 0 if frac == "0" else len(frac), False


def interpretar(token, decimal):
    """Devuelve (valor, decimales_mostrados, es_porcentaje) o None si el formato no encaja con el separador."""
    t = token.replace("−", "-").replace(" ", "")
    pct = t.endswith("%")
    t = t.rstrip("%")
    miles = "." if decimal == "," else ","
    entero, _, frac = t.partition(decimal)
    if decimal in frac:
        return None
    signo = -1 if entero.startswith("-") else 1
    entero = entero.lstrip("+-")
    if miles in entero:
        grupos = entero.split(miles)
        if not (1 <= len(grupos[0]) <= 3 and all(len(g) == 3 for g in grupos[1:])):
            return None  # «3.14» con decimal «,»: no es separador de miles
        entero = "".join(grupos)
    if not entero.isdigit() or (frac and not frac.isdigit()):
        return None
    return signo * float(f"{entero}.{frac or 0}"), len(frac), pct


def numeros(ruta, decimal, ignorar=()):
    """Itera (valor, token, lugar, contexto). Un archivo estructurado se lee celda por celda: un número nativo se toma
    tal cual y una celda de texto se interpreta con el separador declarado. La prosa pasa por la expresión regular."""
    if ruta.suffix.lower() not in ESTRUCTURADOS:
        yield from numeros_texto(texto_de(ruta), decimal, ignorar)
        return
    try:
        lista = list(celdas(ruta))
    except (json.JSONDecodeError, csv.Error) as e:
        print(f"Aviso: {ruta.name} no se pudo leer como {ruta.suffix} ({e}); se lee como texto.", file=sys.stderr)
        yield from numeros_texto(texto_de(ruta), decimal, ignorar)
        return
    for lugar, c in lista:
        if c is None or isinstance(c, bool):
            continue
        if isinstance(c, (int, float)):
            yield nativo(c), repr(c), lugar, repr(c)
            continue
        c = str(c).strip()
        if ignorar and any(pat.search(c) for pat in ignorar):
            continue
        if NUMERO.fullmatch(c):
            yield interpretar(c, decimal), c, lugar, c
        else:
            for v, token, _, ctx in numeros_texto(c, decimal, ignorar):
                yield v, token, lugar, ctx


def numeros_texto(texto, decimal, ignorar=()):
    """Itera (valor, token, número de línea, contexto) en prosa."""
    for n, linea in enumerate(texto.splitlines(), 1):
        limpia = FECHAS.sub(lambda m: " " * len(m.group()), linea)
        for pat in ignorar:
            limpia = pat.sub(lambda m: " " * len(m.group()), limpia)
        for m in NUMERO.finditer(limpia):
            token = m.group().rstrip(".,")  # un punto o una coma final es puntuación de la frase
            ctx = linea[max(0, m.start() - 30):m.end() + 30].strip()
            yield interpretar(token, decimal), token, n, ctx


def valores_fuente(rutas, decimal):
    valores, donde = [], {}
    archivos = []
    for r in map(Path, rutas):
        archivos += sorted(p for p in r.rglob("*") if p.is_file()) if r.is_dir() else [r]
    legibles = [a for a in archivos if a.suffix.lower() in LEIBLES]
    if not legibles:
        print("Aviso: no se encontraron archivos legibles en las fuentes indicadas.", file=sys.stderr)
    for a in legibles:
        for v, _, n, _ in numeros(a, decimal):
            if v is not None:
                valores.append(v[0])
                donde.setdefault(v[0], f"{a.name}:{n}")
    valores.sort()
    return valores, donde


def buscar(valores, objetivo, tolerancia):
    i = bisect.bisect_left(valores, objetivo - tolerancia)
    j = bisect.bisect_right(valores, objetivo + tolerancia)
    return valores[i:j]


def trivial(valor, decimales, pct, token):
    if pct or decimales or any(s in token for s in ".,"):
        return False
    return 0 <= valor <= 9 or 1900 <= valor <= 2100


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entregables", nargs="+")
    p.add_argument("--fuentes", nargs="+", required=True)
    p.add_argument("--decimal", choices=[".", ","], required=True)
    p.add_argument("--decimal-fuentes", choices=[".", ","], default=".")
    p.add_argument("--escala", type=float, action="append", default=[])
    p.add_argument("--ignorar", action="append", default=[],
                   help="expresión regular a ignorar en el entregable (repetible)")
    p.add_argument("--todas", action="store_true", help="lista también las encontradas")
    a = p.parse_args()

    ignorar = []
    for patron in a.ignorar:
        try:
            ignorar.append(re.compile(patron))
        except re.error as e:
            raise SystemExit(f"Expresión regular inválida en --ignorar ({patron!r}): {e}")

    for r in map(Path, [*a.entregables, *a.fuentes]):
        if not r.exists():
            raise SystemExit(f"No existe la ruta: {r}. Revisá el nombre o el directorio de trabajo.")

    valores, donde = valores_fuente(a.fuentes, a.decimal_fuentes)
    grupos = {"huérfanas": [], "ambiguas": [], "encontradas": [], "triviales": []}
    for ent in map(Path, a.entregables):
        for v, token, n, ctx in numeros(ent, a.decimal, ignorar):
            lugar = f"{ent.name}:{n}"
            if v is None:
                grupos["ambiguas"].append((token, lugar, ctx, ""))
                continue
            valor, dec, pct = v
            if trivial(valor, dec, pct, token):
                grupos["triviales"].append((token, lugar, ctx, ""))
                continue
            tol = 0.5 * 10 ** -dec + 1e-9
            pruebas = [(valor, tol)] + [(valor * e, tol * e) for e in a.escala]
            if pct:
                pruebas.append((valor / 100, tol / 100))
            hallados = [h for obj, t in pruebas for h in buscar(valores, obj, t)]
            if hallados:
                grupos["encontradas"].append((token, lugar, ctx, f"{donde[hallados[0]]} ({len(hallados)} lugares)"))
            else:
                grupos["huérfanas"].append((token, lugar, ctx, ""))

    print(f"# Cifras: {', '.join(Path(e).name for e in a.entregables)}\n")
    nota_ignorar = f", ignorando {len(ignorar)} patrón(es)" if ignorar else ""
    print(f"Fuentes: {len(valores)} valores numéricos. Decimal del entregable «{a.decimal}», "
          f"de las fuentes «{a.decimal_fuentes}»" + (f", escalas {a.escala}" if a.escala else "") + nota_ignorar + ".\n")
    print(" · ".join(f"{k}: {len(v)}" for k, v in grupos.items()) + "\n")
    for nombre in ("huérfanas", "ambiguas") + (("encontradas",) if a.todas else ()):
        if grupos[nombre]:
            print(f"## {nombre.capitalize()}\n")
            print("| Cifra | Dónde | Contexto | Fuente |\n|---|---|---|---|")
            for token, lugar, ctx, fuente in grupos[nombre]:
                print(f"| {token} | {lugar} | {ctx.replace('|', '/')} | {fuente} |")
            print()
    if grupos["triviales"]:
        print("Triviales (no verificadas): " + ", ".join(sorted({t for t, *_ in grupos["triviales"]})))
    sys.exit(1 if grupos["huérfanas"] or grupos["ambiguas"] else 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    main()
