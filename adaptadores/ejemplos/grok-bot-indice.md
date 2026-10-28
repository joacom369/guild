# Índice para el perfil de Grok Bot

Bloque para pegar en el perfil o la memoria del bot, cuando las `description` de los oficios no llegan solas.
Es un índice: la tabla completa está en [`AGENTS.md`](../../AGENTS.md) y las reglas anti-pisado, en
[`../grok-bot.md`](../grok-bot.md). Acá no se reescriben.

No está instalado en ningún bot. Pegarlo es decisión de quien configura el ambiente.

## Bloque

```markdown
## Skills Guild

Índice de oficios. Si el pedido coincide con un momento, leé el `SKILL.md` de ese oficio (o cargalo como skill)
antes de seguir. La tabla completa está en `AGENTS.md`.

- Empezar, retomar o cerrar un proyecto o un trabajo de varios pasos: `foreman`.
- Plantear, interpretar un resultado o concluir: `provenance`. Elegir técnica: `compass`.
- Pedir agentes, repartir o cuidar el costo: `tokenwise`. Abrir opciones: `lenses`.
- Sacar datos: `quarry`. Analizar: `assay`. Construir un entregable: `kiln`. Verificar cifras: `hallmark`.
- Escribir afuera o borrar: `herald`. Una tarea que se repite: `foundry`. Ponerse al día con las fuentes: `sherpa`.
- Pulir una interfaz: `impeccable` (la usa `kiln`). Dirección visual: `design-taste-frontend`, sólo si se la nombra.

Al abrir (primera respuesta del turno, mensaje de despertar o rutina): buzón, mediciones vencidas y `ESTADO.md`.
Si hay novedad, una línea.

Antes de un `Task`, aplicá la sección «Reglas anti-pisado» de `adaptadores/grok-bot.md`: un workstream es un
`executor` reutilizado, sin fan-out sin permiso del usuario, `computerUse` de a uno, el código de un repo en
CloudAgent, y escribir afuera sólo con `herald` (`DraftExternalMessage` hasta el sí).

La rutina de mejora corre `python foundry/scripts/auditar_gremio.py --dinamico --al-buzon`. Propone en el buzón.
No edita skills ni lee sesiones. El ciclo está en `foundry/referencias/harness-autoauditoria.md`.
```
