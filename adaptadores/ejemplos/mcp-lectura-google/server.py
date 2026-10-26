"""Servidor MCP de sólo lectura para Gmail y Google Calendar.

Los permisos que se piden a Google son de lectura (gmail.readonly, calendar.readonly):
aunque alguien lo intentara, con este token no se puede mandar, borrar ni modificar nada.

Uso:
  python server.py --autorizar   # una vez: abre el navegador para dar permiso
  python server.py               # lo lanza Claude Code (stdio)
"""

import base64
import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from mcp.server import MCPServer

AQUI = Path(__file__).parent
CLIENTE = AQUI / "client_secret.json"
TOKEN = AQUI / "token.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]


def credenciales():
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES) if TOKEN.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN.write_text(creds.to_json())
    if not creds or not creds.valid:
        raise RuntimeError("Falta autorizar: corré `python server.py --autorizar`.")
    return creds


def gmail():
    return build("gmail", "v1", credentials=credenciales(), cache_discovery=False)


def calendar():
    return build("calendar", "v3", credentials=credenciales(), cache_discovery=False)


def encabezados(msg, nombres=("From", "To", "Cc", "Subject", "Date")):
    h = {x["name"]: x["value"] for x in msg.get("payload", {}).get("headers", [])}
    return {n: h[n] for n in nombres if n in h}


def cuerpo(payload):
    """Texto plano del mensaje; si sólo hay HTML, le saca las etiquetas."""
    partes, html = [payload], None
    while partes:
        p = partes.pop(0)
        partes.extend(p.get("parts", []))
        data = p.get("body", {}).get("data")
        if not data:
            continue
        texto = base64.urlsafe_b64decode(data).decode("utf-8", "replace")
        if p.get("mimeType") == "text/plain":
            return texto
        if p.get("mimeType") == "text/html" and html is None:
            html = re.sub(r"<[^>]+>", " ", texto)
    return html or ""


mcp = MCPServer("google-lectura", instructions="Gmail y Calendar del usuario, sólo lectura.")


@mcp.tool()
def quien_soy() -> dict:
    """Cuenta autorizada: dirección de Gmail y calendario principal. Usar antes de leer."""
    perfil = gmail().users().getProfile(userId="me").execute()
    principal = calendar().calendars().get(calendarId="primary").execute()
    return {"gmail": perfil["emailAddress"], "calendario_principal": principal["id"]}


@mcp.tool()
def buscar_correos(consulta: str, maximo: int = 20) -> list[dict]:
    """Busca hilos con la sintaxis de Gmail (from:, subject:, after:AAAA/MM/DD, "Q604294"...).
    Devuelve id del hilo, encabezados y resumen de su último mensaje."""
    g = gmail()
    hilos = g.users().threads().list(userId="me", q=consulta, maxResults=min(maximo, 50)).execute()
    salida = []
    for t in hilos.get("threads", []):
        h = g.users().threads().get(userId="me", id=t["id"], format="metadata").execute()
        ultimo = h["messages"][-1]
        salida.append({"hilo": t["id"], "mensajes": len(h["messages"]),
                       **encabezados(ultimo), "resumen": ultimo.get("snippet", "")})
    return salida


@mcp.tool()
def leer_hilo(hilo: str, max_caracteres: int = 6000) -> list[dict]:
    """Lee todos los mensajes de un hilo (encabezados y texto, recortado por mensaje)."""
    h = gmail().users().threads().get(userId="me", id=hilo, format="full").execute()
    return [{**encabezados(m), "texto": cuerpo(m["payload"])[:max_caracteres]} for m in h["messages"]]


@mcp.tool()
def listar_calendarios() -> list[dict]:
    """Calendarios que el usuario ve en su lista."""
    items = calendar().calendarList().list().execute().get("items", [])
    return [{"id": c["id"], "nombre": c.get("summary"), "principal": c.get("primary", False)} for c in items]


@mcp.tool()
def listar_eventos(desde: str, hasta: str, calendario: str = "primary", maximo: int = 50) -> list[dict]:
    """Eventos entre dos momentos RFC 3339 con zona (p. ej. 2026-10-26T00:00:00-03:00)."""
    items = calendar().events().list(
        calendarId=calendario, timeMin=desde, timeMax=hasta, singleEvents=True,
        orderBy="startTime", maxResults=min(maximo, 250)).execute().get("items", [])
    return [{
        "titulo": e.get("summary", "(sin título)"),
        "inicio": e["start"].get("dateTime", e["start"].get("date")),
        "fin": e["end"].get("dateTime", e["end"].get("date")),
        "lugar": e.get("location"),
        "enlace_reunion": e.get("hangoutLink"),
        "organizador": e.get("organizer", {}).get("email"),
        "mi_respuesta": next((a.get("responseStatus") for a in e.get("attendees", []) if a.get("self")), None),
        "invitados": len(e.get("attendees", [])),
    } for e in items]


if __name__ == "__main__":
    if "--autorizar" in sys.argv:
        flujo = InstalledAppFlow.from_client_secrets_file(CLIENTE, SCOPES)
        TOKEN.write_text(flujo.run_local_server(port=0, open_browser=True).to_json())
        print("Autorizado. Token guardado en", TOKEN)
    else:
        mcp.run()
