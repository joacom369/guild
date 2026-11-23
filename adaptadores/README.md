# Adaptadores

El núcleo (los oficios, el mapa, los scripts) es texto y Python, y no depende de ninguna IA. Lo que sí cambia de una
plataforma a otra es **cómo se cargan los oficios, dónde viven las reglas, qué pasa al abrir una sesión, cómo se
lanzan agentes, cómo se programa una rutina y cómo se conectan las fuentes del usuario**. Eso es el adaptador.

El contrato que cumple cada adaptador, con el estado de cada plataforma, está en
[`mapa/MAPA.md`](../mapa/MAPA.md) §6. En cada necesidad se marca «probado» sólo lo que se usó de verdad.

| Plataforma | Archivo | Estado |
|---|---|---|
| Claude Code (y claude.ai para las skills sueltas) | [`claude-code.md`](claude-code.md) | En uso; el hook y la rutina, sin probar |
| Google Antigravity (2.0 / IDE / CLI) | [`antigravity.md`](antigravity.md) | Diseñado y documentado; skills globales y cuotas probadas |
| Cualquier plataforma que lea `AGENTS.md` (Cursor, Codex y otras) | [`../AGENTS.md`](../AGENTS.md) | Escrito, sin probar (manifiestos [`.agents/skills.json`](../.agents/skills.json), [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json) y [`.cursor-plugin/plugin.json`](../.cursor-plugin/plugin.json), documentados) |
| Bot en servidor propio (Grok Bot) | [`grok-bot.md`](grok-bot.md) | Diseñado y documentado, sin probar |

## Cómo se escribe un adaptador nuevo

1. Recorré la tabla del contrato y, para cada necesidad, buscá el mecanismo de la plataforma. Si no lo tiene, anotá
   «no soporta» y qué se pierde.
2. Escribí el adaptador como `adaptadores/<plataforma>.md`: cómo se instala, dónde van las reglas, cómo se resuelve
   cada necesidad.
3. Probalo con un trabajo real y recién ahí marcá «probado» en el contrato.
4. **No edites los oficios para que encajen en la plataforma.** Si un oficio necesita algo que la plataforma no da,
   eso es una necesidad del contrato, no un cambio del núcleo.

## Ejemplos reutilizables

- [`ejemplos/mcp-lectura-google/`](ejemplos/mcp-lectura-google/): un servidor MCP local de **sólo lectura** para Gmail
  y Google Calendar, con credencial propia. Sirve en cualquier plataforma que hable MCP. Es la receta de
  [`quarry/referencias/conectores.md`](../quarry/referencias/conectores.md) llevada a código.
