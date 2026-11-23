# Adaptador: Claude Code (y claude.ai)

Probado en Claude Code (Windows) entre el 2026-10-15 y el 2026-10-26.

## Instalar

**Clonando** (recomendado para quien lo mantiene): las skills quedan donde Claude Code las busca.

```bash
git clone https://github.com/joacom369/guild.git ~/.claude/skills
```

Si `~/.claude/skills` ya existe, clonar aparte y copiar las carpetas.

**Como plugins**, desde el catálogo del repositorio (`.claude-plugin/marketplace.json`):

```
/plugin marketplace add joacom369/guild
/plugin install foreman@guild
```

Igual para `provenance`, `compass`, `tokenwise`, `lenses`, `herald`, `quarry`, `assay`, `kiln`, `hallmark`, `foundry`, `sherpa`,
`impeccable` y `design-taste-frontend`. Desde la versión 2.1.275 también sirve
`/plugin install <skill> --marketplace joacom369/guild`. El repositorio es privado: la PC necesita acceso a GitHub
con la cuenta que tiene permiso (por ejemplo, `gh auth login`).

**En claude.ai:** `python empaquetar.py` arma `dist/<skill>.zip`; se sube en Configuración > Capacidades > Skills.

## Cómo resuelve el contrato

| Necesidad del núcleo | En Claude Code |
|---|---|
| Saber qué oficio cargar y cuándo | La `description` de cada skill, más un índice corto en `~/.claude/CLAUDE.md` |
| Cargar un procedimiento a demanda | Skill: `SKILL.md` y sus `referencias/` |
| Reglas que valen siempre | `~/.claude/CLAUDE.md` (usuario) y `CLAUDE.md` del proyecto |
| Algo que pasa al abrir la sesión | Hook `SessionStart` (ver abajo; **no instalado**: es decisión del usuario) |
| Agente con una tarea | Subagente; el encargo lo escribe `tokenwise` |
| Varios agentes en orden fijo | Workflow (sólo si el usuario lo pide) |
| Correr solo, con horario | Rutina programada (`/schedule`) |
| Conectores del usuario | Conectores de claude.ai, plugins con OAuth por máquina o MCP locales (ver abajo) |

## El índice en CLAUDE.md

Un bloque corto que nombre cada oficio y su momento. Por ejemplo:

```markdown
## Skills propias (en ~/.claude/skills)
- Trabajo analítico: `provenance` al plantear y antes de concluir; en orden `compass` → `quarry` → `assay` → `kiln` → `hallmark`.
- Antes de lanzar subagentes o repartir una tarea de tres o más partes: `tokenwise`.
- Una tarea que se repite: `foundry`. Ponerse al día con el chat y el correo: `sherpa`.
- Empezar, retomar o cerrar un proyecto: `foreman`.
```

## Hook de inicio de sesión (opcional, sin probar)

No está instalado ni probado dentro de `settings.json`; sólo se probó el comando suelto. Para que `foreman` avise del buzón al abrir cada sesión, en `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
        "command": "python -c \"import pathlib,sys;sys.stdout.reconfigure(encoding='utf-8');p=pathlib.Path.home()/'.foreman'/'IDEAS.md';n=sum('| nueva |' in l for l in p.read_text(encoding='utf-8').splitlines()) if p.exists() else 0;print(f'foreman: hay {n} ideas nuevas en el buzón') if n else None\"" } ] }
    ]
  }
}
```

## Conectores con la cuenta del usuario

En una cuenta de claude.ai compartida, sus conectores pueden ser de otra persona. Lo que funcionó (2026-10-26):

- **Chat (Slack):** el conector del plugin `sales` se autoriza por máquina (OAuth). Se activa al llamar su herramienta
  `authenticate`; después se verifica el perfil.
- **Correo y calendario (Google):** los servidores MCP oficiales de Google piden que el proyecto esté inscripto en un
  programa de vista previa, y no aceptan el registro automático de clientes. Lo que sí funcionó fue un MCP local de
  sólo lectura con una credencial OAuth propia:
  [`ejemplos/mcp-lectura-google/`](ejemplos/mcp-lectura-google/).
- **GitHub:** el MCP oficial (`https://api.githubcopilot.com/mcp/`) con un `headersHelper` que le pide el token a
  `gh auth token --user <cuenta>`. Así el token no queda escrito en la configuración.

Los comandos útiles:

```bash
claude mcp add -s user <nombre> -- <python del entorno> <ruta>/server.py        # MCP local
claude mcp add-json -s user <nombre> '{"type":"http","url":"<url>","headersHelper":"<comando>"}'
claude mcp list                                                                 # «Connected» no prueba la identidad
```

Después de agregar un servidor, `/reload-plugins` y una lectura real para verificar de quién es la cuenta.

## Notas de Windows (PowerShell 5.1)

- **UTF-8 sin BOM:** `Get-Content` sin `-Encoding UTF8` seguido de `Out-File` (o `>`) rompe acentos de archivos UTF-8 sin BOM; usar `[IO.File]::ReadAllText` / `[IO.File]::WriteAllText` (con `[Text.UTF8Encoding]::new($false)`) o Python con `encoding="utf-8"`.
- **Alias `R`:** una función auxiliar llamada `R` choca con el alias integrado de `Invoke-History` y falla en silencio sin tocar archivos; usar nombres largos.
- **Skill externa `pptx`:** `scripts/office/validate.py` falla en Windows al no hallar sus esquemas XSD; validar abriendo en PowerPoint o en Linux/WSL y dejarlo asentado en el acta de `hallmark`.
