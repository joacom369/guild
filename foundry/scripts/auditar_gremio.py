"""Audita el gremio: estático (oficios) y, con --dinamico, propuestas a partir del trabajo hecho.

Uso:
    python foundry/scripts/auditar_gremio.py [--raiz RUTA] [--estricto]
    python foundry/scripts/auditar_gremio.py --dinamico [--registros DIR] [--trabajo DIR] [--al-buzon] [--hoy FECHA]
    python foundry/scripts/auditar_gremio.py --autoprueba

El paso estático lee los SKILL.md, AGENTS.md y la tabla de dueños de mapa/MAPA.md §3.
No mide tasas de disparo: eso lo controla empaquetar.py (el piso sólo sube).

El paso dinámico lee los registros del ambiente (delegaciones, tramos, lecciones,
automatizaciones, buzón). Propone mejoras comunes y puntuales. No edita skills y no
abre sesiones: mirar el historial pide el permiso de foreman (su regla 6).

Sale 0 si el reporte se pudo armar. Con --estricto sale 1 si hay un hallazgo de
nivel error (falta el caso negativo o falta el piso en una skill propia).
--autoprueba siembra fallas y un trabajo de ejemplo, y sale 1 si un detector no dispara.
Los solapes y las propuestas son avisos: una pista para leer, no un fallo cerrado.
"""
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

TERCEROS = {"impeccable", "design-taste-frontend"}
# Nombrados en el mapa como oficios que no viven en este repositorio.
EXTERNOS = {"ponytail", "dataviz"}

MIN_PALABRAS_ENUNCIADO = 12
# 0,72 alcanza para ver una frase casi copiada; por debajo aparecen parecidos de tema, no de regla.
RATIO_ENUNCIADO = 0.72
VENTANA = 10
MIN_CONTENIDO_VENTANA = 4
# Un token entra al solape si aparece en pocas descriptions (no es muletilla del gremio).
DF_MAX = 3
MIN_TOKENS_AVISO = 2
# El paso dinámico: cuántas veces tiene que repetirse un hecho para proponerlo.
REPETICION_PEDIDO = 3
REPETICION_FALTA = 2
MIN_FILAS_SIN_COMPROBACION = 3
ALIASES_DELEGACION = {
    "pedido": ("pedido", "para que", "tarea"),
    "oficio": ("oficio", "agente", "quien", "skill"),
    "usado": ("se uso", "usado", "uso"),
    "comprobacion": ("comprobacion", "prueba"),
    "falto": ("que falto", "falto", "herramienta"),
}

STOP = {
    "para", "como", "cuando", "donde", "qué", "que", "cuál", "cual", "cuáles", "cuales",
    "cómo", "con", "sin", "sobre", "entre", "desde", "hasta", "hacia", "por", "una", "uno",
    "unas", "unos", "del", "los", "las", "les", "este", "esta", "esto", "esa", "ese", "eso",
    "cada", "todo", "toda", "todos", "todas", "muy", "más", "mas", "menos", "también",
    "tambien", "solo", "sólo", "ya", "hay", "ser", "son", "está", "están", "sus", "ella",
    "ellos", "ellas", "algo", "alguien", "nada", "mismo", "misma", "otros", "otras", "otro",
    "otra", "puede", "pueden", "hace", "hacer", "tiene", "tienen", "usar", "usado", "dice",
    "pedir", "pide", "usuario", "usuarios", "skill", "skills", "oficio", "oficios", "trabajo",
    "trabajos", "pedido", "pedidos", "antes", "después", "despues", "siempre", "nunca",
    "donde", "the", "and", "for", "with", "when", "that", "this", "from", "not", "use",
    "user", "into", "your", "only", "also", "its", "are", "was", "you", "want", "wants",
    "should", "would", "there", "their", "about", "which", "while", "have", "been",
    "cada", "otro", "otra", "donde", "quien", "quién", "porque", "pero", "aunque",
    "durante", "mediante", "según", "segun", "hacia", "contra", "bajo", "tras", "pues",
    "entonces", "además", "ademas", "cualquier", "cualquiera", "mismo", "misma",
}

# Verbos y sustantivos que aparecen en cualquier description y no identifican un momento.
GENERICOS = {
    "empezar", "empieza", "punto", "puntos", "fijos", "fijo", "busca", "buscar",
    "parte", "partes", "vista", "cuenta", "cuentas", "escribe", "escribir",
    "prueba", "probar", "termina", "terminar", "archivo", "archivos", "estado",
    "sesion", "codigo", "intento", "intentos", "revisa", "revisar", "contrato",
    "pregunta", "preguntas", "resultado", "resultados", "salida", "salidas",
    "herramienta", "herramientas", "costo", "costos", "construir", "construye",
    "conviene", "agente", "agentes", "tarea", "tareas", "varia", "varias", "varios",
    "grande", "control", "controles", "procedimiento", "sistema", "sistemas",
    "numero", "proyecto", "proyectos", "cambia", "cambiar", "entrega", "entregar",
    "entregable", "primer", "primera", "dentro", "fuera", "forma", "formas",
    "manera", "nivel", "tipo", "tipos", "caso", "casos", "paso", "pasos", "fase",
    "fases", "hecho", "mejor", "nuevo", "nueva", "cierra", "cerrar", "abre",
    "abrir", "final", "propia", "propio", "ajena", "ajeno", "nombre", "usando",
    "usuario", "oficio", "skill", "skills", "trabajo", "trabajos", "pedido",
    "pedidos", "cuando", "donde", "antes", "despues", "siempre", "tambien",
    "hacer", "tiene", "puede", "queda", "dejar", "decir", "dice", "pide",
    "decision", "decisiones",
}

NEGACION = re.compile(r"\b(no|tampoco|not|neither)\b", re.I)
REF_SKILL = re.compile(r"`([A-Za-z][A-Za-z0-9_.-]*)`")
NOMBRE_SKILL = re.compile(r"^[a-z][a-z0-9-]+$")


class Hallazgo:
    def __init__(self, nivel, tipo, titulo, detalle):
        self.nivel = nivel
        self.tipo = tipo
        self.titulo = titulo
        self.detalle = detalle

    def linea(self):
        cuerpo = f"[{self.nivel}] {self.tipo}: {self.titulo}"
        if self.detalle:
            cuerpo += "\n    " + self.detalle.replace("\n", "\n    ")
        return cuerpo


def raiz_por_defecto():
    return Path(__file__).resolve().parents[2]


def plegar(texto):
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def normalizar(texto):
    texto = re.sub(r"`([^`]*)`", r" \1 ", texto)
    texto = re.sub(r"\[([^\]]+)\]\([^)]*\)", r" \1 ", texto)
    texto = re.sub(r"[*_#>\[\]]", " ", texto)
    texto = plegar(texto)
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def canon(tok):
    """Junta plurales obvios (tableros/tablero) sin comerse palabras en -sis."""
    if len(tok) > 5 and tok.endswith("es") and tok[-3] not in "aeiou":
        return tok[:-2]
    if len(tok) > 5 and tok.endswith("s") and not tok.endswith("sis"):
        return tok[:-1]
    return tok


def tokens(texto):
    """Palabras del texto, sin muletillas. El plural se junta después, al comparar."""
    palabras = re.findall(r"[a-z]{5,}", plegar(texto))
    return [p for p in palabras if p not in STOP and p not in GENERICOS and canon(p) not in GENERICOS]


def sin_cercas(texto):
    return re.sub(r"```.*?```", " ", texto, flags=re.S)


def partir_frontmatter(texto):
    if not texto.startswith("---"):
        return {}, texto
    fin = texto.find("\n---", 3)
    if fin < 0:
        return {}, texto
    return texto[3:fin], texto[fin + 4:]


def valor_clave(crudo, clave):
    """Valor de una clave simple del frontmatter, incluida la description plegada con > o |."""
    lineas = crudo.splitlines()
    for i, linea in enumerate(lineas):
        if not linea.startswith(clave + ":"):
            continue
        resto = linea[len(clave) + 1:].strip()
        if resto in {">", "|", ">-", "|-", ">+", "|+"}:
            partes = []
            for sig in lineas[i + 1:]:
                if sig.startswith((" ", "\t")):
                    partes.append(sig.strip())
                elif sig.strip() == "":
                    partes.append("")
                else:
                    break
            return re.sub(r"\s+", " ", " ".join(p for p in partes if p)).strip()
        if len(resto) >= 2 and resto[0] == resto[-1] and resto[0] in "\"'":
            return resto[1:-1]
        return resto
    return ""


def cargar_skills(raiz):
    skills = []
    for carpeta in sorted(p for p in raiz.iterdir() if p.is_dir()):
        archivo = carpeta / "SKILL.md"
        if not archivo.exists():
            continue
        texto = archivo.read_text(encoding="utf-8")
        crudo, cuerpo = partir_frontmatter(texto)
        nombre = valor_clave(crudo, "name") or carpeta.name
        skills.append({
            "nombre": carpeta.name,
            "nombre_frontmatter": nombre,
            "carpeta": carpeta.name,
            "description": valor_clave(crudo, "description"),
            "cuerpo": cuerpo,
            "solo_por_nombre": valor_clave(crudo, "disable-model-invocation").lower() == "true",
            "tercero": carpeta.name in TERCEROS,
            "evals": carpeta / "evals",
            "piso": carpeta / "evals" / "piso.json",
        })
    return skills


def cortar_negativo(description):
    """El caso negativo es el último enunciado que empieza con No/Tampoco/Not, no un «no» del medio."""
    cortes = list(re.finditer(r"(?:^|[.])\s+(No\b|Tampoco\b|Not\b)", description))
    if not cortes:
        return description, ""
    corte = cortes[-1]
    return description[:corte.start() + 1].strip(), description[corte.start():].strip()


def zona_disparo(description):
    """Oraciones que dicen cuándo cargar la skill.

    Entran el «Usar…» / «Use when», las que traen un ejemplo entre comillas y, después del
    «Usar», las que son una lista (dos comas o más: «landing, dashboards, product UI»).
    """
    pre, _ = cortar_negativo(description)
    oraciones = [o.strip() for o in re.split(r"(?<=[.!?])\s+", pre) if o.strip()]
    tomadas = []
    vio_usar = False
    for oracion in oraciones:
        es_usar = re.search(r"\b(Usar|Use when|Use for)\b", oracion) is not None
        tiene_comillas = re.search(r"[«“\"]", oracion) is not None
        es_lista = oracion.count(",") >= 2
        if es_usar or tiene_comillas or (vio_usar and es_lista):
            tomadas.append(oracion)
        vio_usar = vio_usar or es_usar
    return " ".join(tomadas) if tomadas else pre


def preambulo(description):
    pre, _ = cortar_negativo(description)
    marca = re.search(r"\b(Usar|Use when|Use for)\b", pre)
    return pre[:marca.start()] if marca else ""


def refs_negativas(description, propio):
    _, cola = cortar_negativo(description)
    return {r for r in REF_SKILL.findall(cola) if NOMBRE_SKILL.match(r) and r != propio}


def caso_negativo(skill):
    if skill["tercero"]:
        return None
    descripcion = skill["description"]
    if not descripcion:
        return Hallazgo("error", "caso negativo", skill["nombre"], "no tiene description")
    if not NEGACION.search(descripcion):
        return Hallazgo(
            "error", "caso negativo", skill["nombre"],
            "la description no dice cuándo no cargar esta skill",
        )
    if not refs_negativas(descripcion, skill["nombre"]):
        return Hallazgo(
            "error", "caso negativo", skill["nombre"],
            "niega, pero no nombra al oficio dueño entre comillas invertidas (por ejemplo `compass`)",
        )
    return None


def por_canon(toks):
    return {canon(t): t for t in toks}


def solapes_de_momento(skills):
    piezas = []
    hallazgos = []
    for skill in skills:
        if skill["solo_por_nombre"]:
            hallazgos.append(Hallazgo(
                "info", "robo de momento", skill["nombre"],
                "disable-model-invocation: no compite por el disparo; se carga sólo por nombre",
            ))
            continue
        disparo = set(tokens(zona_disparo(skill["description"])))
        anclas = {t for t in tokens(preambulo(skill["description"])) if len(canon(t)) >= 6}
        piezas.append((skill, disparo, anclas, disparo | anclas))
    frecuencia = {}
    for _, _, _, todos in piezas:
        for clave in por_canon(todos):
            frecuencia[clave] = frecuencia.get(clave, 0) + 1
    for i, (a, da, _, ta) in enumerate(piezas):
        ca, da_c = por_canon(ta), por_canon(da)
        for b, db, _, tb in piezas[i + 1:]:
            cb, db_c = por_canon(tb), por_canon(db)
            claves = sorted(
                k for k in ca.keys() & cb.keys()
                if frecuencia.get(k, 0) <= DF_MAX and k not in {a["nombre"], b["nombre"]}
            )
            if not claves:
                continue
            en_disparo = [k for k in claves if k in da_c and k in db_c]
            cruzado = [k for k in claves if len(k) >= 7 and ((k in da_c) ^ (k in db_c))]
            compartidos = [ca[k] if len(ca[k]) <= len(cb[k]) else cb[k] for k in claves]
            se_nombran = (
                b["nombre"] in refs_negativas(a["description"], a["nombre"])
                or a["nombre"] in refs_negativas(b["description"], b["nombre"])
            )
            # Un aviso pide dos palabras en el «Usar…», una palabra larga ahí, cuatro en el
            # preámbulo, o una palabra larga que está en el «Usar…» de una y en el preámbulo de la otra.
            fuerte = (
                len(en_disparo) >= MIN_TOKENS_AVISO
                or any(len(k) >= 8 for k in en_disparo)
                or len(claves) >= 4
                or bool(cruzado)
            )
            if not fuerte and not (se_nombran and len(claves) >= 3):
                continue
            if se_nombran and len(claves) < 3 and len(en_disparo) < MIN_TOKENS_AVISO:
                continue
            nivel = "info" if se_nombran or not fuerte else "aviso"
            nota = "el caso negativo ya nombra al otro" if se_nombran else "ninguno nombra al otro en el caso negativo"
            if en_disparo:
                donde = "en el «Usar…»"
            elif cruzado:
                donde = "una en el «Usar…» y la otra en el preámbulo"
            else:
                donde = "en el preámbulo, no en el «Usar…»"
            hallazgos.append(Hallazgo(
                nivel, "robo de momento",
                f"{a['nombre']} × {b['nombre']}",
                f"{nota} ({donde}). Palabras: {', '.join(compartidos)}",
            ))
    return hallazgos


def enunciados(cuerpo):
    limpio = sin_cercas(cuerpo)
    salida = []
    for trozo in re.split(r"\n+", limpio):
        trozo = trozo.strip()
        if not trozo or trozo.startswith("#"):
            continue
        for parte in re.split(r"(?<=[.!?])\s+", trozo):
            norma = normalizar(parte)
            if len(norma.split()) >= MIN_PALABRAS_ENUNCIADO:
                salida.append(norma)
    return salida


def contenido(norma):
    return {w for w in norma.split() if w not in STOP and len(w) >= 4}


def reglas_duplicadas(skills):
    por_skill = [(s["nombre"], enunciados(s["cuerpo"])) for s in skills if not s["tercero"]]
    vistos = []
    for i, (na, ea) in enumerate(por_skill):
        for nb, eb in por_skill[i + 1:]:
            mejor = None
            for a in ea:
                ca = contenido(a)
                if len(ca) < 4:
                    continue
                for b in eb:
                    if len(ca & contenido(b)) < 4:
                        continue
                    ratio = SequenceMatcher(None, a, b).ratio()
                    if ratio >= RATIO_ENUNCIADO and (mejor is None or ratio > mejor[0]):
                        mejor = (ratio, a, b)
            if mejor:
                ratio, a, b = mejor
                vistos.append(Hallazgo(
                    "aviso", "regla duplicada",
                    f"{na} × {nb} ({ratio:.0%})",
                    f"«{a[:180]}»\n«{b[:180]}»",
                ))
    ventanas = {}
    for skill in skills:
        if skill["tercero"]:
            continue
        palabras = normalizar(sin_cercas(skill["cuerpo"])).split()
        for i in range(0, max(0, len(palabras) - VENTANA + 1)):
            ventana = tuple(palabras[i:i + VENTANA])
            if sum(1 for w in ventana if w not in STOP and len(w) >= 4) < MIN_CONTENIDO_VENTANA:
                continue
            ventanas.setdefault(ventana, set()).add(skill["nombre"])
    pares = {}
    for ventana, nombres in ventanas.items():
        if len(nombres) < 2:
            continue
        nombres = sorted(nombres)
        for i, na in enumerate(nombres):
            for nb in nombres[i + 1:]:
                pares.setdefault((na, nb), ventana)
    ya = {(h.titulo.split(" (")[0]) for h in vistos}
    for (na, nb), ventana in sorted(pares.items()):
        clave = f"{na} × {nb}"
        if clave in ya:
            continue
        texto = " ".join(ventana)
        vistos.append(Hallazgo(
            "aviso", "regla duplicada",
            f"{na} × {nb} (ventana igual)",
            f"«{texto}»",
        ))
    return vistos


def piso_faltante(skills):
    hallazgos = []
    for skill in skills:
        if skill["tercero"]:
            continue
        if not skill["piso"].exists():
            donde = "no tiene evals/" if not skill["evals"].exists() else "tiene evals/ pero no piso.json"
            hallazgos.append(Hallazgo(
                "error", "piso", skill["nombre"],
                f"{donde}. Las propias del gremio guardan la tasa en evals/piso.json; el control de tasas es empaquetar.py",
            ))
    return hallazgos


def tabla(texto, titulo_seccion, titulo_siguiente):
    inicio = texto.find(titulo_seccion)
    if inicio < 0:
        return None
    fin = texto.find(titulo_siguiente, inicio + len(titulo_seccion))
    bloque = texto[inicio:fin if fin > 0 else None]
    filas = []
    for linea in bloque.splitlines():
        if not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if not celdas or set(celdas[0]) <= {"-", " "}:
            continue
        if celdas[0].lower() in {"regla", "momento", "necesidad del núcleo", "plataforma"}:
            continue
        filas.append(celdas)
    return filas


def dueños(raiz, skills):
    hallazgos = []
    mapa = raiz / "mapa" / "MAPA.md"
    if not mapa.exists():
        return [Hallazgo("error", "dueños", "MAPA.md", "no está mapa/MAPA.md")]
    texto = mapa.read_text(encoding="utf-8")
    filas = tabla(texto, "## 3. Un dueño por regla", "## 4.")
    if not filas:
        return [Hallazgo("error", "dueños", "MAPA §3", "no se pudo leer la tabla de dueños")]
    carpetas = {s["carpeta"] for s in skills}
    vistas = {}
    for celdas in filas:
        regla = celdas[0]
        dueno = celdas[1] if len(celdas) > 1 else ""
        clave = normalizar(regla)
        vistas.setdefault(clave, []).append(dueno)
        for ref in REF_SKILL.findall(dueno):
            if not NOMBRE_SKILL.match(ref):
                continue
            if ref in EXTERNOS:
                hallazgos.append(Hallazgo(
                    "info", "dueño", ref,
                    f"oficio externo: la tabla §3 lo nombra dueño de «{regla}» y no vive en este repositorio",
                ))
                continue
            if ref in carpetas:
                continue
            hallazgos.append(Hallazgo(
                "aviso", "dueño", ref,
                f"la tabla §3 lo nombra dueño de «{regla}» y no hay carpeta ni está en la lista de oficios externos ({', '.join(sorted(EXTERNOS))})",
            ))
    for clave, duenos in vistas.items():
        if len(duenos) < 2:
            continue
        hallazgos.append(Hallazgo(
            "aviso", "dueño repetido", clave[:80],
            "la misma regla aparece en más de una fila: " + " · ".join(duenos),
        ))
    return hallazgos


def indice(raiz, skills):
    hallazgos = []
    archivo = raiz / "AGENTS.md"
    if not archivo.exists():
        return [Hallazgo("error", "índice", "AGENTS.md", "no está en la raíz")]
    texto = archivo.read_text(encoding="utf-8")
    filas = tabla(texto, "## Qué oficio y cuándo", "## Herramientas")
    if not filas:
        return [Hallazgo("error", "índice", "AGENTS.md", "no se pudo leer la tabla de oficios")]
    nombrados = set()
    momentos = []
    for celdas in filas:
        if len(celdas) < 2:
            continue
        momento, oficio = celdas[0], celdas[1]
        for ref in REF_SKILL.findall(oficio):
            if NOMBRE_SKILL.match(ref):
                nombrados.add(ref)
                momentos.append((ref, momento))
        for ruta in re.findall(r"\]\(([^)]+)\)", " ".join(celdas)):
            if ruta.startswith("http"):
                continue
            destino = (raiz / ruta).resolve()
            if not destino.exists():
                hallazgos.append(Hallazgo("error", "índice", ruta, "AGENTS.md apunta a un archivo que no está"))
    for skill in skills:
        if skill["tercero"] or skill["carpeta"] in nombrados:
            continue
        hallazgos.append(Hallazgo(
            "aviso", "índice", skill["nombre"],
            "tiene SKILL.md y no aparece en la tabla de AGENTS.md",
        ))
    frecuencia = {}
    tokenizados = []
    for nombre, momento in momentos:
        toks = set(tokens(momento))
        tokenizados.append((nombre, toks))
        for tok in toks:
            frecuencia[tok] = frecuencia.get(tok, 0) + 1
    for i, (na, ta) in enumerate(tokenizados):
        for nb, tb in tokenizados[i + 1:]:
            compartidos = sorted(t for t in ta & tb if frecuencia.get(t, 0) <= DF_MAX)
            if len(compartidos) < MIN_TOKENS_AVISO:
                continue
            hallazgos.append(Hallazgo(
                "aviso", "índice solapado", f"{na} × {nb}",
                "palabras del momento en AGENTS.md: " + ", ".join(compartidos),
            ))
    return hallazgos


def auditar(raiz):
    raiz = Path(raiz)
    skills = cargar_skills(raiz)
    hallazgos = []
    if not skills:
        hallazgos.append(Hallazgo("error", "raíz", str(raiz), "no hay carpetas con SKILL.md"))
    for skill in skills:
        hallazgo = caso_negativo(skill)
        if hallazgo:
            hallazgos.append(hallazgo)
    hallazgos.extend(solapes_de_momento(skills))
    hallazgos.extend(reglas_duplicadas(skills))
    hallazgos.extend(piso_faltante(skills))
    hallazgos.extend(dueños(raiz, skills))
    hallazgos.extend(indice(raiz, skills))
    return skills, hallazgos


def formatear(raiz, skills, hallazgos):
    orden = {"error": 0, "aviso": 1, "info": 2}
    hallazgos = sorted(hallazgos, key=lambda h: (h.tipo, orden.get(h.nivel, 9), h.titulo))

    def contar(tipo, nivel=None):
        return sum(1 for h in hallazgos if h.tipo == tipo and (nivel is None or h.nivel == nivel))

    resumen = (
        f"caso negativo: {contar('caso negativo')} error; "
        f"piso: {contar('piso')} error; "
        f"robo de momento: {contar('robo de momento', 'aviso')} aviso, {contar('robo de momento', 'info')} info; "
        f"reglas duplicadas: {contar('regla duplicada')}; "
        f"dueños: {contar('dueño') + contar('dueño repetido')}; "
        f"índice: {contar('índice') + contar('índice solapado')}"
    )
    lineas = [
        "Auditoría del gremio",
        f"Raíz: {raiz}",
        f"Skills leídas: {len(skills)} ({', '.join(s['nombre'] for s in skills)})",
        "Resumen: " + resumen,
        "",
    ]
    if not hallazgos:
        lineas.append("Sin hallazgos.")
    else:
        tipo = None
        for h in hallazgos:
            if h.tipo != tipo:
                tipo = h.tipo
                lineas.append(f"## {tipo}")
            lineas.append(h.linea())
            lineas.append("")
    lineas.append(
        "Lectura: un error es una skill propia sin caso negativo o sin piso. "
        "Un aviso es una pista (solape o texto casi igual). "
        "Un info es un solape que el caso negativo ya cubre, una skill que sólo se carga por nombre, "
        "o un dueño externo que el mapa ya nombra. "
        "Las tasas de disparo las controla empaquetar.py."
    )
    return "\n".join(lineas).rstrip() + "\n"


class Propuesta:
    def __init__(self, clase, titulo, porque, evidencia, area):
        self.clase = clase
        self.titulo = titulo
        self.porque = porque
        self.evidencia = evidencia
        self.area = area
        self.omitida = ""

    def linea(self):
        if self.omitida:
            return f"[info] omitida: {self.titulo}\n    ya estaba descartada ({self.omitida})"
        return f"[aviso] {self.clase}: {self.titulo}\n    {self.porque} Evidencia: {self.evidencia}"


def argumento(argv, nombre):
    if nombre not in argv:
        return None
    i = argv.index(nombre)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        return None
    return argv[i + 1]


def leer_tablas(texto):
    """Tablas markdown como lista de filas (dict encabezado → celda)."""
    tablas, bloque = [], []

    def cerrar():
        nonlocal bloque
        if len(bloque) >= 2 and set(bloque[1].replace("|", "").replace(":", "")) <= set("- "):
            encabezados = [c.strip() for c in bloque[0].strip().strip("|").split("|")]
            filas = []
            for linea in bloque[2:]:
                celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
                celdas += [""] * (len(encabezados) - len(celdas))
                filas.append(dict(zip(encabezados, celdas)))
            if filas:
                tablas.append(filas)
        bloque = []

    for linea in texto.splitlines():
        if linea.startswith("|"):
            bloque.append(linea)
        else:
            cerrar()
    cerrar()
    return tablas


def campos_delegacion(fila):
    campos = {}
    for clave, valor in fila.items():
        encabezado = plegar(clave)
        for nombre, alias in ALIASES_DELEGACION.items():
            if any(opcion == encabezado or opcion in encabezado for opcion in alias):
                campos.setdefault(nombre, valor)
    return campos


def leer_texto(path):
    path = Path(path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def delegaciones(texto):
    filas = []
    for tabla in leer_tablas(texto):
        for fila in tabla:
            campos = campos_delegacion(fila)
            if campos.get("pedido") or campos.get("oficio"):
                filas.append(campos)
    return filas


def es_no(valor):
    texto = plegar(valor or "").strip()
    return texto in {"no", "no se uso", "no usado"} or texto.startswith("no ")


def seccion(texto, titulo):
    marca = f"## {titulo}"
    inicio = texto.find(marca)
    if inicio < 0:
        return ""
    resto = texto[inicio + len(marca):]
    fin = resto.find("\n## ")
    return resto if fin < 0 else resto[:fin]


def ideas_descartadas(texto):
    pares = []
    for tabla in leer_tablas(texto):
        for fila in tabla:
            idea, estado = "", ""
            for clave, valor in fila.items():
                encabezado = plegar(clave)
                if encabezado.startswith("idea"):
                    idea = valor
                elif "estado" in encabezado:
                    estado = valor
            if idea and "descartada" in plegar(estado):
                pares.append((idea, estado))
    return pares


def ya_descartada(propuesta, descartadas):
    texto = normalizar(propuesta.titulo)
    for idea, estado in descartadas:
        frase = normalizar(idea)
        if len(frase) >= 12 and frase in texto:
            return estado
    return ""


def propuestas_de_delegaciones(filas):
    propuestas = []
    if not filas:
        return propuestas
    sin_comprobacion = [f for f in filas if not (f.get("comprobacion") or "").strip()]
    if len(sin_comprobacion) >= MIN_FILAS_SIN_COMPROBACION:
        propuestas.append(Propuesta(
            "común",
            f"{len(sin_comprobacion)} encargos del registro no traen una comprobación que el agente pueda correr",
            "Una comprobación en el encargo sube el resultado de todos los subagentes: se corrigen antes de devolver. Cómo se escribe el encargo es de `tokenwise` §3.",
            f"{len(sin_comprobacion)} filas sin comprobación",
            "común",
        ))
    pedidos = Counter(normalizar(f.get("pedido", "")) for f in filas if len(normalizar(f.get("pedido", ""))) >= 12)
    for pedido, veces in sorted(pedidos.items()):
        if veces >= REPETICION_PEDIDO:
            propuestas.append(Propuesta(
                "común",
                f"El pedido «{pedido}» aparece {veces} veces",
                "Es una tarea repetida. La mira `foundry`; este script no arma la automatización.",
                f"{veces} delegaciones con el mismo pedido",
                "común",
            ))
    faltas = {}
    for fila in filas:
        falta = normalizar(fila.get("falto", ""))
        if len(falta) < 8:
            continue
        oficio = (fila.get("oficio") or "sin oficio").strip()
        faltas.setdefault(falta, Counter())[oficio] += 1
    for falta, por_oficio in sorted(faltas.items()):
        oficios = [o for o, n in por_oficio.items() if n >= 1]
        if len(oficios) >= 2:
            propuestas.append(Propuesta(
                "común",
                f"En más de un oficio faltó «{falta}»",
                "Una herramienta o un paso compartido les serviría a esos subagentes. No se agrega solo.",
                ", ".join(f"{o} ×{por_oficio[o]}" for o in sorted(por_oficio)),
                "común",
            ))
        else:
            oficio, veces = next(iter(por_oficio.items()))
            if veces >= REPETICION_FALTA:
                propuestas.append(Propuesta(
                    "puntual",
                    f"`{oficio}`: faltó «{falta}» {veces} veces",
                    "Una mejora en ese oficio cambiaría el resultado que recibe el usuario. No se editó la skill.",
                    f"{oficio} ×{veces}",
                    oficio,
                ))
    no_usados = Counter((f.get("oficio") or "").strip() for f in filas if es_no(f.get("usado", "")))
    for oficio, veces in sorted(no_usados.items()):
        if oficio and veces >= REPETICION_FALTA:
            propuestas.append(Propuesta(
                "puntual",
                f"`{oficio}`: {veces} resultados no se usaron",
                "El encargo está trayendo material que después no entra. Ajustar qué devuelve ese agente ahorra la cuota y mejora lo que llega al usuario. El formato del encargo es de `tokenwise` §3.",
                f"{oficio}: se usó = no, {veces} veces",
                oficio,
            ))
    return propuestas


def propuestas_de_estado(texto, origen):
    propuestas = []
    abiertos = {}
    for linea in seccion(texto, "Tramos").splitlines():
        if not linea.strip().startswith("-"):
            continue
        marca = re.search(r"qued[oó] abierto\s+(.+)$", linea, re.I)
        if not marca:
            continue
        frase = marca.group(1).strip()
        clave = normalizar(frase)
        veces, _ = abiertos.get(clave, (0, frase))
        abiertos[clave] = (veces + 1, frase)
    for clave, (veces, frase) in sorted(abiertos.items()):
        if veces >= REPETICION_FALTA and len(clave) >= 8:
            propuestas.append(Propuesta(
                "resultado",
                f"Quedó abierto «{frase}» en {veces} tramos",
                "Es un hueco del resultado, no de un solo encargo. Cerrarlo cambia lo que el usuario recibe al final.",
                f"{origen}, sección Tramos",
                "resultado",
            ))
    for linea in seccion(texto, "Lecciones de método").splitlines():
        if not linea.strip().startswith("-"):
            continue
        oficio = re.search(r"oficio\s+`?([a-z][a-z0-9-]*)`?", linea, re.I)
        if not oficio:
            continue
        nombre = oficio.group(1)
        propuestas.append(Propuesta(
            "puntual",
            f"`{nombre}`: {linea.strip().lstrip('-').strip()[:140]}",
            "La lección ya está escrita como método. Pasarla al oficio, si el usuario la aprueba, mejora el trabajo de ese agente.",
            f"{origen}, sección Lecciones de método",
            nombre,
        ))
    return propuestas


def mediciones_vencidas(texto, hoy):
    propuestas = []
    for tabla in leer_tablas(texto):
        for fila in tabla:
            nombre, medicion = "", ""
            for clave, valor in fila.items():
                encabezado = plegar(clave)
                if "automatizacion" in encabezado or encabezado == "nombre":
                    nombre = valor
                elif "medicion" in encabezado:
                    medicion = valor
            marca = re.search(r"pendiente:\s*(\d{4}-\d{2}-\d{2})", medicion or "")
            if not marca:
                continue
            cuando = date.fromisoformat(marca.group(1))
            if cuando < hoy:
                propuestas.append(Propuesta(
                    "resultado",
                    f"Medición vencida: {nombre or 'automatización'} (pendiente {cuando.isoformat()})",
                    "`foundry` pide comparar la predicción con lo que pasó. Sin esa medición no se sube de escalón.",
                    "AUTOMATIZACIONES.md",
                    "foundry",
                ))
    return propuestas


def auditar_dinamico(registros, trabajo=None, hoy=None):
    """Propuestas a partir de los registros. No lee sesiones ni edita skills."""
    registros = Path(registros)
    hoy = hoy or date.today()
    notas, propuestas = [], []
    if not registros.exists() and not trabajo:
        return [], [f"Sin registros en {registros}. No se leyeron sesiones. No hay propuestas."]
    if registros.exists():
        filas = delegaciones(leer_texto(registros / "DELEGACIONES.md"))
        if filas:
            propuestas.extend(propuestas_de_delegaciones(filas))
        else:
            notas.append("DELEGACIONES.md no está o no tiene filas reconocibles.")
        propuestas.extend(mediciones_vencidas(leer_texto(registros / "AUTOMATIZACIONES.md"), hoy))
        descartadas = ideas_descartadas(leer_texto(registros / "IDEAS.md"))
    else:
        notas.append(f"Sin registros en {registros}.")
        descartadas = []
    if trabajo:
        camino = Path(trabajo)
        estados = [camino] if camino.is_file() else sorted(camino.rglob("ESTADO.md"))
        if not estados:
            notas.append(f"No hay ESTADO.md en {camino}.")
        for estado in estados:
            propuestas.extend(propuestas_de_estado(leer_texto(estado), estado.name))
    for propuesta in propuestas:
        propuesta.omitida = ya_descartada(propuesta, descartadas)
    return propuestas, notas


def formatear_dinamico(registros, propuestas, notas):
    lineas = [
        "## Dinámico",
        f"Registros: {registros}",
        "No se leyeron sesiones ni se editó ninguna skill. Cada propuesta espera el buzón y la aprobación.",
        "",
    ]
    for nota in notas:
        lineas.append(nota)
    if not propuestas:
        lineas.append("Sin propuestas.")
    else:
        for propuesta in propuestas:
            lineas.append(propuesta.linea())
            lineas.append("")
    lineas.append(
        "Común: el mismo hueco en más de un oficio, o un encargo que se repite. "
        "Puntual: un solo oficio. Resultado: un tramo que queda abierto o una medición vencida."
    )
    return "\n".join(lineas).rstrip() + "\n"


ENCABEZADO_BUZON = (
    "| Fecha | Área | Idea | Por qué importa | Estado (nueva / charlada / aprobada / aplicada / descartada) |\n"
    "|---|---|---|---|---|\n"
)


def volcar_buzon(archivo, propuestas, hoy):
    """Agrega al buzón las propuestas nuevas. No toca las descartadas ni edita skills."""
    archivo = Path(archivo)
    archivo.parent.mkdir(parents=True, exist_ok=True)
    previo = archivo.read_text(encoding="utf-8") if archivo.exists() else ""
    if "| Fecha |" not in previo:
        previo = (previo.rstrip() + "\n\n" + ENCABEZADO_BUZON) if previo.strip() else ENCABEZADO_BUZON
    plano = normalizar(previo)
    nuevas = []
    for propuesta in propuestas:
        if propuesta.omitida:
            continue
        titulo = propuesta.titulo.replace("|", "/")
        if normalizar(titulo) in plano:
            continue
        porque = propuesta.porque.replace("|", "/")
        nuevas.append(
            f"| {hoy.isoformat()} | {propuesta.area} | {titulo} | {porque} | nueva |\n"
        )
        plano += " " + normalizar(titulo)
    if nuevas:
        archivo.write_text(previo.rstrip() + "\n" + "".join(nuevas), encoding="utf-8")
    return len(nuevas)


def autoprueba():
    """Siembra fallas conocidas y comprueba que cada detector las ve."""
    fallo = []
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / "mapa").mkdir()
        (raiz / "alfa").mkdir()
        (raiz / "beta" / "evals").mkdir(parents=True)
        (raiz / "gamma" / "evals").mkdir(parents=True)
        (raiz / "alfa" / "SKILL.md").write_text(
            "---\nname: alfa\ndescription: Se usa al contar las nubes del inventario forestal de altura.\n---\n\n"
            "# Alfa\n\nCuenta nubes.\n",
            encoding="utf-8",
        )
        regla = (
            "Cada semilla del inventario se anota con su fecha de cosecha y su lote de origen antes de cerrar el parte diario.\n"
        )
        (raiz / "beta" / "SKILL.md").write_text(
            "---\nname: beta\ndescription: Usar al armar el tablero comercial semanal del deposito. No decide la técnica (`compass`).\n---\n\n"
            "# Beta\n\n" + regla,
            encoding="utf-8",
        )
        (raiz / "gamma" / "SKILL.md").write_text(
            "---\nname: gamma\ndescription: Usar al armar el tablero comercial semanal de la sucursal. No construye la página (`kiln`).\n---\n\n"
            "# Gamma\n\n" + regla,
            encoding="utf-8",
        )
        (raiz / "beta" / "evals" / "piso.json").write_text("{}\n", encoding="utf-8")
        (raiz / "mapa" / "MAPA.md").write_text(
            "## 3. Un dueño por regla\n\n"
            "| Regla | Dueño | Los demás… |\n|---|---|---|\n"
            "| La misma regla inventada de los semilleros | `beta` | — |\n"
            "| La misma regla inventada de los semilleros | `gamma` | — |\n"
            "| Código mínimo inventado | `ponytail` | — |\n"
            "| Dueño fantasma del semillero | `noexiste` | — |\n\n"
            "## 4. Otra\n",
            encoding="utf-8",
        )
        (raiz / "AGENTS.md").write_text(
            "## Qué oficio y cuándo\n\n"
            "| Momento | Oficio | Leer |\n|---|---|---|\n"
            "| Armar el tablero comercial semanal | `beta` | [`beta/SKILL.md`](beta/SKILL.md) |\n"
            "| Armar el tablero comercial semanal de la sucursal | `gamma` | [`gamma/SKILL.md`](gamma/SKILL.md) |\n"
            "| Archivo que no está | `beta` | [`beta/NO.md`](beta/NO.md) |\n\n"
            "## Herramientas\n",
            encoding="utf-8",
        )
        _, hallazgos = auditar(raiz)
        texto = "\n".join(h.linea() for h in hallazgos)

        def espera(fragmento, porque):
            if fragmento not in texto:
                fallo.append(f"{porque}: no apareció «{fragmento}»")

        espera("[error] caso negativo: alfa", "caso negativo")
        espera("[error] piso: alfa", "piso ausente")
        espera("[aviso] robo de momento: beta × gamma", "solape de momento")
        espera("[aviso] regla duplicada: beta × gamma", "regla duplicada")
        espera("[aviso] dueño repetido:", "misma regla, dos filas")
        espera("[aviso] dueño: noexiste", "dueño que no está")
        espera("[aviso] índice: alfa", "skill fuera del índice")
        espera("[error] índice: beta/NO.md", "enlace roto")
        espera("[aviso] índice solapado: beta × gamma", "momentos del índice")
        if "ponytail" in texto and "[aviso] dueño: ponytail" in texto:
            fallo.append("ponytail está en la lista de externos y no debería avisarse")
        if fallo:
            print(texto)
            print("AUTOPRUEBA FALLÓ")
            for item in fallo:
                print(" -", item)
            return 1
    if autoprueba_dinamica():
        return 1
    print("Autoprueba: los detectores vieron las fallas sembradas (caso negativo, piso, solape, regla duplicada, dueños, índice, propuestas dinámicas).")
    return 0


def autoprueba_dinamica():
    """Un trabajo sembrado: mejoras comunes, puntuales, una descartada y el buzón que no pisa."""
    fallo = []
    hoy = date(2026, 10, 28)
    with tempfile.TemporaryDirectory() as tmp:
        registros = Path(tmp) / "foreman"
        registros.mkdir()
        (registros / "DELEGACIONES.md").write_text(
            "| Fecha | Oficio | Pedido | Se usó | Comprobación | Qué faltó |\n"
            "|---|---|---|---|---|---|\n"
            "| 2026-10-01 | quarry | extraer lotes del norte | no | | |\n"
            "| 2026-10-02 | quarry | cruzar lotes del sur | no | | |\n"
            "| 2026-10-03 | kiln | armar la pagina del lote | sí | | exportar a planilla |\n"
            "| 2026-10-04 | hallmark | revisar la pagina del lote | sí | | exportar a planilla |\n"
            "| 2026-10-05 | assay | revisar el parte diario | sí | | |\n"
            "| 2026-10-06 | kiln | revisar el parte diario | sí | | |\n"
            "| 2026-10-07 | herald | revisar el parte diario | sí | | |\n"
            "| 2026-10-08 | assay | calcular el margen semanal | sí | | |\n"
            "| 2026-10-09 | kiln | calcular el margen semanal | sí | | |\n"
            "| 2026-10-10 | quarry | calcular el margen semanal | sí | | |\n",
            encoding="utf-8",
        )
        (registros / "IDEAS.md").write_text(
            "| Fecha | Área | Idea | Por qué importa | Estado (nueva / charlada / aprobada / aplicada / descartada) |\n"
            "|---|---|---|---|---|\n"
            "| 2026-09-01 | foundry | calcular el margen semanal | ya se miró | descartada: no se repite de verdad |\n",
            encoding="utf-8",
        )
        (registros / "AUTOMATIZACIONES.md").write_text(
            "| Fecha | Automatización | Escalón | Tarea que reemplaza | Predicción (fechada) | Lentes que aportaron | Medición |\n"
            "|---|---|---|---|---|---|---|\n"
            "| 2026-09-01 | resumen diario | 7 rutina | repaso | Ahorra 10 min | vago | pendiente: 2026-10-01 |\n",
            encoding="utf-8",
        )
        estado = Path(tmp) / "ESTADO.md"
        estado.write_text(
            "# Estado\n\n## Tramos\n"
            "- 2026-10-20 · salió el perfil · quedó abierto el cruce de lotes\n"
            "- 2026-10-27 · salió la página · quedó abierto el cruce de lotes\n\n"
            "## Lecciones de método\n"
            "- El oficio kiln entregó la página sin la cifra de origen.\n",
            encoding="utf-8",
        )
        propuestas, _ = auditar_dinamico(registros, estado, hoy)
        texto = formatear_dinamico(registros, propuestas, [])

        def espera(fragmento, porque):
            if fragmento not in texto:
                fallo.append(f"{porque}: no apareció «{fragmento}»")

        espera("No se leyeron sesiones ni se editó ninguna skill", "el dinámico no edita")
        espera("[aviso] común: ", "mejora común")
        espera("comprobación que el agente pueda correr", "comprobación")
        espera("exportar a planilla", "herramienta compartida")
        espera("revisar el parte diario", "tarea repetida")
        espera("[aviso] puntual: `quarry`:", "resultados no usados")
        espera("[aviso] puntual: `kiln`:", "lección de un oficio")
        espera("[aviso] resultado: Quedó abierto «el cruce de lotes»", "tramo abierto")
        espera("Medición vencida: resumen diario", "predicción vencida")
        espera("[info] omitida:", "no repetir descartada")
        if any("calcular el margen semanal" in p.titulo and not p.omitida for p in propuestas):
            fallo.append("se volvió a proponer un pedido descartado")
        escritas = volcar_buzon(registros / "IDEAS.md", propuestas, hoy)
        otra = volcar_buzon(registros / "IDEAS.md", propuestas, hoy)
        buzon = (registros / "IDEAS.md").read_text(encoding="utf-8")
        if escritas < 5:
            fallo.append(f"el buzón recibió {escritas} filas, se esperaban varias")
        if otra != 0:
            fallo.append("la segunda volcada duplicó propuestas")
        if buzon.count("descartada:") != 1:
            fallo.append("se pisó la idea descartada")
        if "exportar a planilla" not in buzon:
            fallo.append("la mejora común no llegó al buzón")
    if fallo:
        print("AUTOPRUEBA DINÁMICA FALLÓ")
        for item in fallo:
            print(" -", item)
        return 1
    return 0


def main(argv):
    if "--autoprueba" in argv:
        return autoprueba()
    estricto = "--estricto" in argv
    raiz = raiz_por_defecto()
    if "--raiz" in argv:
        raiz = Path(argumento(argv, "--raiz"))
    skills, hallazgos = auditar(raiz)
    sys.stdout.write(formatear(raiz, skills, hallazgos))
    if "--dinamico" in argv:
        registros = Path(argumento(argv, "--registros") or (Path.home() / ".foreman"))
        hoy_texto = argumento(argv, "--hoy")
        hoy = date.fromisoformat(hoy_texto) if hoy_texto else date.today()
        propuestas, notas = auditar_dinamico(registros, argumento(argv, "--trabajo"), hoy)
        sys.stdout.write("\n")
        sys.stdout.write(formatear_dinamico(registros, propuestas, notas))
        if "--al-buzon" in argv:
            if registros.exists():
                n = volcar_buzon(registros / "IDEAS.md", propuestas, hoy)
                sys.stdout.write(f"Buzón: {n} propuestas nuevas. Ninguna skill se editó.\n")
            else:
                sys.stdout.write(f"Buzón: no se escribió; no está {registros}.\n")
    errores = [h for h in hallazgos if h.nivel == "error"]
    if not skills:
        return 2
    if estricto and errores:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
