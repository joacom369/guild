"""Audita el gremio en estático: caso negativo, solapes de momento, reglas casi iguales y piso.

Uso:
    python foundry/scripts/auditar_gremio.py [--raiz RUTA] [--estricto]
    python foundry/scripts/auditar_gremio.py --autoprueba

Lee los SKILL.md, el índice AGENTS.md y la tabla de dueños de mapa/MAPA.md §3.
No mide tasas de disparo: eso lo controla empaquetar.py (el piso sólo sube).

Sale 0 si el reporte se pudo armar. Con --estricto sale 1 si hay un hallazgo de
nivel error (falta el caso negativo o falta el piso en una skill propia).
--autoprueba siembra un gremio con fallas conocidas y sale 1 si un detector no dispara.
Los solapes son avisos: una pista para leer, no un fallo cerrado.
"""
import re
import sys
import tempfile
import unicodedata
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
    print("Autoprueba: los detectores vieron las fallas sembradas (caso negativo, piso, solape, regla duplicada, dueños, índice).")
    return 0


def main(argv):
    if "--autoprueba" in argv:
        return autoprueba()
    estricto = "--estricto" in argv
    raiz = raiz_por_defecto()
    if "--raiz" in argv:
        raiz = Path(argv[argv.index("--raiz") + 1])
    skills, hallazgos = auditar(raiz)
    sys.stdout.write(formatear(raiz, skills, hallazgos))
    errores = [h for h in hallazgos if h.nivel == "error"]
    if not skills:
        return 2
    if estricto and errores:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
