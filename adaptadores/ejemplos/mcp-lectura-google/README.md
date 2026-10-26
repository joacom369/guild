# MCP de sólo lectura para Gmail y Google Calendar

Un servidor MCP local, de unas 120 líneas, que le da a cualquier agente compatible con MCP cinco herramientas:
`quien_soy`, `buscar_correos`, `leer_hilo`, `listar_calendarios` y `listar_eventos`.

**Los permisos que se piden a Google son de lectura** (`gmail.readonly`, `calendar.readonly`): con ese token no se
puede mandar, borrar ni modificar nada, aunque el código lo intentara.

## Cuándo conviene

Cuando el conector de la plataforma está autenticado como otra persona, o cuando los servidores oficiales no están
disponibles para tu cuenta. La receta general está en
[`quarry/referencias/conectores.md`](../../../quarry/referencias/conectores.md).

## Instalar

1. **Credencial propia en Google Cloud** (una vez):
   - un proyecto nuevo, con **Gmail API** y **Google Calendar API** habilitadas;
   - pantalla de consentimiento de tipo **Interno** si la cuenta es de una organización;
   - credencial **ID de cliente de OAuth**, tipo **App de escritorio**. Descargá el JSON.
2. **Carpeta fuera del repositorio** (la credencial y el token no se versionan):

   ```bash
   mkdir -p ~/.mcp/google-lectura && cp server.py requirements.txt ~/.mcp/google-lectura/
   cp <descargado>.json ~/.mcp/google-lectura/client_secret.json
   cd ~/.mcp/google-lectura
   python -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt      # en Windows: .venv/Scripts/python.exe
   ```

3. **Autorizar** (abre el navegador; entrá con tu cuenta y fijate que pida sólo «ver»):

   ```bash
   .venv/bin/python server.py --autorizar
   ```

4. **Registrar el servidor en la plataforma.** Por ejemplo, en Claude Code:

   ```bash
   claude mcp add -s user google-lectura -- <ruta>/.venv/bin/python <ruta>/server.py
   ```

5. **Verificar:** llamá `quien_soy` y comprobá que la dirección sea la tuya antes de leer nada.

## Lo que hay que saber

- `token.json` da acceso de lectura a tu correo: no lo compartas ni lo subas a un repositorio.
- Si el token vence o se revoca, repetí el paso 3.
- Hecho con `mcp` 2.x (`from mcp.server import MCPServer`). En la versión 1 la clase se llamaba `FastMCP`.
