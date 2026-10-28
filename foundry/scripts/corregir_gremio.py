"""Corrige lo mecánico del índice. No toca skills.

Uso:
    python foundry/scripts/corregir_gremio.py [--raiz RUTA]
    python foundry/scripts/corregir_gremio.py --aplicar [--raiz RUTA]
    python foundry/scripts/corregir_gremio.py --autoprueba

Reescribe un enlace roto de la tabla de AGENTS.md («Qué oficio y cuándo») sólo cuando
hay un único archivo con ese nombre. Sin --aplicar no escribe.

No edita un SKILL.md, no crea evals/piso.json y no cambia dueños. Un caso negativo,
un piso o una description los deja el auditor en error: son un corte, y este script
no los baja de nivel.
"""
import re
import sys
import tempfile
from pathlib import Path

ENLACE = re.compile(r"\]\(([^)]+)\)")
IGNORAR = {".git", "__pycache__", "dist"}


def raiz_por_defecto():
    return Path(__file__).resolve().parents[2]


def seccion_indice(texto):
    inicio = texto.find("## Qué oficio y cuándo")
    if inicio < 0:
        return None
    fin = texto.find("## Herramientas", inicio + 1)
    if fin < 0:
        fin = len(texto)
    return inicio, fin


def resolver(raiz, ruta):
    """ok, externo, unico o corte. unico trae la ruta nueva."""
    if ruta.startswith(("http://", "https://")):
        return "externo", None
    partes = Path(ruta).parts
    if not ruta or ruta.startswith("/") or ".." in partes:
        return "corte", "la ruta sale del repositorio"
    destino = (raiz / ruta)
    if destino.is_file():
        return "ok", None
    nombre = Path(ruta).name
    if not nombre or nombre in {".", ".."}:
        return "corte", "sin nombre de archivo"
    hallados = []
    for camino in raiz.rglob(nombre):
        if not camino.is_file():
            continue
        if any(parte in IGNORAR for parte in camino.parts):
            continue
        hallados.append(camino)
    if len(hallados) == 1:
        nuevo = hallados[0].relative_to(raiz).as_posix()
        if nuevo == ruta:
            return "corte", "no está"
        return "unico", nuevo
    if not hallados:
        return "corte", "no hay otro archivo con ese nombre"
    return "corte", f"{len(hallados)} archivos se llaman {nombre}; no elijo"


def corregir(raiz, texto):
    """Devuelve el texto nuevo, las correcciones y los cortes. No escribe."""
    raiz = Path(raiz)
    bounds = seccion_indice(texto)
    if bounds is None:
        return texto, [], ["AGENTS.md no tiene la tabla «Qué oficio y cuándo»"]
    inicio, fin = bounds
    cambios, cortes = [], []

    def linea_nueva(linea):
        if not linea.startswith("|"):
            return linea

        def reemplazo(match):
            ruta = match.group(1)
            clase, dato = resolver(raiz, ruta)
            if clase == "unico":
                cambios.append(f"{ruta} → {dato}")
                return f"]({dato})"
            if clase == "corte":
                cortes.append(f"{ruta} ({dato})")
            return match.group(0)

        return ENLACE.sub(reemplazo, linea)

    seccion = "".join(linea_nueva(linea) for linea in texto[inicio:fin].splitlines(keepends=True))
    return texto[:inicio] + seccion + texto[fin:], cambios, cortes


def aplicar(raiz, escribir):
    raiz = Path(raiz)
    archivo = raiz / "AGENTS.md"
    if not archivo.is_file():
        print("Corte: no está AGENTS.md")
        return 0
    texto = archivo.read_text(encoding="utf-8")
    nuevo, cambios, cortes = corregir(raiz, texto)
    for cambio in cambios:
        print(f"Corregido: {cambio}")
    for corte in cortes:
        print(f"Corte: {corte}")
    if not cambios:
        print("Nada mecánico para corregir.")
    if escribir and nuevo != texto:
        archivo.write_text(nuevo, encoding="utf-8")
        print(f"Escrito: {archivo}")
    elif nuevo != texto:
        print("Sin --aplicar no se escribe.")
    return 0


def autoprueba():
    fallo = []
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / "nuevo").mkdir()
        (raiz / "a").mkdir()
        (raiz / "b").mkdir()
        (raiz / "alfa").mkdir()
        (raiz / "beta").mkdir()
        (raiz / "otra").mkdir()
        (raiz / "nuevo" / "unico-semillero.md").write_text("semilla\n", encoding="utf-8")
        (raiz / "a" / "dos.md").write_text("a\n", encoding="utf-8")
        (raiz / "b" / "dos.md").write_text("b\n", encoding="utf-8")
        skill = "---\nname: alfa\ndescription: No decide la técnica (`compass`).\n---\n\n# Alfa\n"
        (raiz / "alfa" / "SKILL.md").write_text(skill, encoding="utf-8")
        (raiz / "beta" / "SKILL.md").write_text(skill, encoding="utf-8")
        (raiz / "otra" / "unica-nota.md").write_text("nota\n", encoding="utf-8")
        agentes = (
            "# Índice\n\n"
            "Ver [`nota`](fuera-de-tabla/unica-nota.md).\n\n"
            "## Qué oficio y cuándo\n\n"
            "Dentro de la sección, ver [`nota`](fuera-de-tabla/unica-nota.md).\n\n"
            "| Momento | Oficio | Leer |\n|---|---|---|\n"
            "| Semilla | `alfa` | [`x`](viejo/unico-semillero.md) |\n"
            "| Dos | `alfa` | [`x`](falta/dos.md) |\n"
            "| Huérfano | `alfa` | [`x`](nada/huerfano.md) |\n"
            "| Skill movida | `alfa` | [`x`](moved/SKILL.md) |\n"
            "| Ya está | `alfa` | [`x`](alfa/SKILL.md) |\n"
            "| Sale | `alfa` | [`x`](../../etc/passwd) |\n\n"
            "## Herramientas\n\n"
            "Después, ver [`nota`](fuera-de-tabla/unica-nota.md).\n"
        )
        (raiz / "AGENTS.md").write_text(agentes, encoding="utf-8")
        nuevo, cambios, cortes = corregir(raiz, agentes)
        if cambios != ["viejo/unico-semillero.md → nuevo/unico-semillero.md"]:
            fallo.append(f"corregió otra cosa: {cambios}")
        for esperado in ("falta/dos.md", "nada/huerfano.md", "moved/SKILL.md", "../../etc/passwd"):
            if not any(item.startswith(esperado) for item in cortes):
                fallo.append(f"no dejó como corte: {esperado}")
        if "fuera-de-tabla/unica-nota.md" not in nuevo:
            fallo.append("reescrito un enlace que no está en la tabla")
        if nuevo.count("nuevo/unico-semillero.md") != 1:
            fallo.append("el enlace único no quedó una sola vez")
        if (raiz / "alfa" / "SKILL.md").read_text(encoding="utf-8") != skill:
            fallo.append("tocó un SKILL.md")
        if (raiz / "AGENTS.md").read_text(encoding="utf-8") != agentes:
            fallo.append("escribió sin --aplicar")
        aplicar(raiz, True)
        escrito = (raiz / "AGENTS.md").read_text(encoding="utf-8")
        if "viejo/unico-semillero.md" in escrito:
            fallo.append("no escribió la corrección")
        if (raiz / "alfa" / "SKILL.md").read_text(encoding="utf-8") != skill:
            fallo.append("al aplicar tocó un SKILL.md")
        otra, cambios2, _ = corregir(raiz, escrito)
        if cambios2 or otra != escrito:
            fallo.append("la segunda corrida no es idempotente")
    if fallo:
        print("AUTOPRUEBA DEL CORRECTOR FALLÓ")
        for item in fallo:
            print(" -", item)
        return 1
    print("Autoprueba: corrige el enlace único, deja los cortes y no toca skills.")
    return 0


def main(argv):
    if "--autoprueba" in argv:
        return autoprueba()
    raiz = raiz_por_defecto()
    if "--raiz" in argv:
        i = argv.index("--raiz")
        raiz = Path(argv[i + 1])
    return aplicar(raiz, "--aplicar" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
