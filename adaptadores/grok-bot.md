# Adaptador: Grok Bot (bot en servidor propio)

Diseñado y documentado el 2026-10-28. **No está probado:** no se corrió un trabajo en un bot. En el contrato
([`mapa/MAPA.md`](../mapa/MAPA.md) §6) cada fila de esta plataforma dice «documentado». «Probado» queda para cuando
alguien use el checklist de abajo en un bot de verdad.

El núcleo no nombra a Grok Bot. Las diferencias de la plataforma están en este archivo.

## Instalar

Hay tres maneras de tener los oficios. Se pueden combinar.

1. **Skills que la plataforma ya carga.** El Skill tool (skills administradas por Cursor) y las skills de usuario de
   un workflow. Si el bot las anuncia por su `description`, ese es el disparo. El índice de abajo refuerza; no
   reemplaza una description que ya llega.
2. **El repositorio, si ya se puede leer.** Cada oficio se carga leyendo `<oficio>/SKILL.md` cuando el momento llega.
   Leer este repositorio para seguir un oficio no es un trabajo de código. Programar en un repositorio va a
   CloudAgent: no se clona un repo en la box del bot para editarlo.
3. **Índice en el perfil.** Grok Bot no tiene `CLAUDE.md`. Las reglas que valen siempre van al perfil o a la memoria
   del bot, más las skills de dominio del ambiente. El bloque para pegar está en
   [`ejemplos/grok-bot-indice.md`](ejemplos/grok-bot-indice.md). La tabla completa de oficios es
   [`AGENTS.md`](../AGENTS.md), en la raíz del repo.

## Cómo resuelve el contrato

| Necesidad del núcleo | En Grok Bot | Estado |
|---|---|---|
| Saber qué oficio cargar y cuándo | La `description`, si el Skill tool la anuncia. Si no, `AGENTS.md` y el bloque del perfil | documentado |
| Cargar un procedimiento a demanda | Skill tool, o leer `SKILL.md` y sus `referencias/` por ruta | documentado |
| Reglas que valen siempre | Perfil y memoria del bot, y las skills de dominio del ambiente | documentado |
| Algo que pasa al abrir la sesión | No hay hook `SessionStart`. Lo hace la primera respuesta del turno, una rutina o el mensaje de despertar | documentado |
| Agente con una tarea | `Task`: `executor` (hacer), `knowledgeWork` (leer y devolver), `computerUse` (la pantalla) | documentado |
| Varios agentes en un orden fijo | No hay workflow nativo. Se encadenan encargos sobre el mismo `executor`. Varios `Task` nuevos son un fan-out | documentado |
| Correr solo, con horario | `UpdateRoutine`: cron, o un disparo de Slack, GitHub o correo. Corre sin una computadora prendida | documentado |
| Conectores del usuario | MCP con la cuenta del usuario (Gmail, Slack, Calendar y los que estén conectados) | documentado |
| Pasos mecánicos | Los mismos scripts Python | documentado |

## Lo que no da igual

- **No hay hook de inicio de sesión.** Si la primera respuesta, la rutina o el mensaje de despertar no hacen el paso
  de apertura de `foreman`, nadie avisa del buzón. El comando de abajo es una receta, no está instalado.
- **No hay `CLAUDE.md`.** Una regla que sólo esté en el `CLAUDE.md` de otro adaptador no llega.
- **`computerUse` es de a uno.** El segundo espera.
- **Tope blando de unos cuatro `executor` a la vez.** Es un límite de esta plataforma, no del núcleo: `tokenwise` no
  pone un tope fijo de agentes ni de tokens. No se midió en esta entrega.
- **El código de un repositorio va a CloudAgent.** Un `executor` no clona el repo en la box para editarlo.
- **No hay `claude plugin eval` en el bot.** Las pruebas de disparo siguen en Claude Code. Acá el control estático es
  `foundry/scripts/auditar_gremio.py` (el ciclo está en
  [`foundry/referencias/harness-autoauditoria.md`](../foundry/referencias/harness-autoauditoria.md)).
- **Un fan-out pide permiso.** Varios `Task` en paralelo no salen solos.
- **Escribir afuera no lo hace el subagente.** El borrador es `DraftExternalMessage`. El envío espera el sí de
  `herald`.

## Abrir la sesión sin hook

`foreman` pide, al empezar, mirar el buzón, las mediciones vencidas y el `ESTADO.md`, y avisar en una línea si hay
novedad. En Grok Bot eso ocurre en la primera respuesta de un turno de trabajo, en el mensaje con el que el bot
despierta, o dentro de la `UpdateRoutine` que corresponde.

Receta para contar ideas nuevas del buzón (el mismo conteo que el adaptador de Claude Code deja como hook sin
instalar). No se probó dentro de un bot:

```bash
python -c "import pathlib,sys;sys.stdout.reconfigure(encoding='utf-8');p=pathlib.Path.home()/'.foreman'/'IDEAS.md';n=sum('| nueva |' in l for l in p.read_text(encoding='utf-8').splitlines()) if p.exists() else 0;print(f'foreman: hay {n} ideas nuevas en el buzón') if n else None"
```

Si `~/.foreman/` está en la máquina del usuario y no en la box, el Shell lleva `machineId`. Si no hay configuración,
valen los valores por defecto de `foreman` (`referencias/ambiente-ejemplo.md`).

## Mapeo de oficios a herramientas

Las reglas de cada oficio siguen siendo suyas. Acá sólo se dice con qué herramienta de Grok Bot se cumplen.

### `foreman`

- **Abrir y cerrar:** el turno principal. Lee el buzón, las mediciones y el `ESTADO.md`, arma el plan y, al cerrar,
  escribe el estado del proyecto.
- **Aprobar un pedido de agentes:** el turno principal, antes de llamar a `Task`. La aprobación es la regla 3 de
  `foreman`; la ficha es la de `tokenwise` §2.

### `tokenwise`

- La ficha se escribe en el turno principal.
- «Pedir agentes» es un `Task` por fila del equipo, después de esa aprobación. Si el pedido es un fan-out (varios
  `Task` a la vez) hace falta el permiso del usuario en este pedido. Si el consumo de cuota es notable, una línea al
  usuario, como dice la ficha: no se frena el trabajo por eso, salvo el fan-out, que sí espera el permiso.
- Investigar o leer mucho material: `knowledgeWork`, o un `executor` liviano. Un cambio en la box: `executor`. La
  pantalla: `computerUse`. Código en un repositorio: CloudAgent.
- El mismo workstream sigue en el mismo agente: `MessageSubagent` con su id. Para frenarlo: `StopSubagent`.

### `herald`

- La vista previa va al chat, con el texto exacto.
- Ejecutar un mensaje que sale de la sesión es dejarlo en `DraftExternalMessage`. No se llama a la herramienta de
  envío hasta la aprobación explícita de esa acción.
- Un subagente puede preparar el texto. No envía.
- Borrar, archivar o pisar sigue el procedimiento de `herald`. La herramienta de la plataforma que borra no se usa
  sin esa aprobación.

### `sherpa`

- A pedido: el turno principal, o un `knowledgeWork` por fuente. El lector devuelve ítems, no un resumen. El cruce lo
  hace el turno principal. El pedido de esos lectores es la ficha de `tokenwise`.
- Programado: `UpdateRoutine` a la hora de la configuración. Entregar el resumen fuera de la sesión usa la
  autorización permanente acotada de `herald` (un destino, un tipo de contenido, una fecha). Sin esa autorización, el
  resumen queda en la sesión.
- Antes de leer cada conector, la identidad de esa cuenta. Cómo se verifica es de `quarry`
  ([`referencias/conectores.md`](../quarry/referencias/conectores.md)). Que una fuente sea del usuario no dice nada de
  las otras.

## Reglas anti-pisado

Dueño: este adaptador. `foreman` y `tokenwise` apuntan acá y no las copian. La fila está en
[`mapa/MAPA.md`](../mapa/MAPA.md) §3.

1. **Un dueño por fase.** Quién trabaja lo decide `foreman` (su tabla de fases). Un `executor` no elige otro oficio
   ni rearma el plan.
2. **Un workstream, un executor.** El mismo trabajo sigue con `MessageSubagent` sobre el mismo id. Un `executor`
   nuevo es otro trabajo, o un fan-out.
3. **Sin fan-out mudo.** Varios `Task` en paralelo salen sólo si el usuario lo permitió en este pedido. El pedido es
   la ficha de `tokenwise` §2. Dentro de un trabajo lo aprueba `foreman` (regla 3).
4. **`computerUse` de a uno.** El segundo espera a que el primero termine, o se frena con `StopSubagent`.
5. **Tope blando: unos cuatro `executor` a la vez.** Si la ficha pide más, se dice y se hace en tandas. No es un
   tope de tokens. No se midió en esta entrega.
6. **Un escritor por archivo.** La regla es de `tokenwise` §1. Acá se aplica así: dos `executor` no editan el mismo
   archivo.
7. **Escribir afuera pasa por `herald`.** Ningún subagente envía. El canal del borrador es `DraftExternalMessage` y
   la aprobación es por acción.
8. **Código de un repositorio, en CloudAgent.** No se clona el repo en la box para que un `executor` lo edite.

## Scripts

Los scripts del núcleo son los mismos. En la box del bot se corren con Shell sin `machineId`. Si hace falta un
archivo de la máquina del usuario, o Chrome para `kiln/scripts/foto_pagina.py`, el Shell lleva `machineId`.

`python foundry/scripts/auditar_gremio.py` usa la biblioteca estándar. Con `--dinamico` lee los registros de
`~/.foreman/` (y un `ESTADO.md` si se le pasa `--trabajo`) y propone mejoras; con `--al-buzon` las agrega al buzón.
No edita skills y no abre sesiones. La cadencia, si se quiere que corra solo, es una `UpdateRoutine`: no está
creada. El ciclo está en
[`foundry/referencias/harness-autoauditoria.md`](../foundry/referencias/harness-autoauditoria.md).
`foto_pagina.py` necesita Chrome y
`websockets`; `openpyxl` hace falta para `.xlsx`. No se miró qué hay instalado en una box de Grok Bot. La corrida del
auditor que figura en el informe se hizo en la máquina donde se escribió este adaptador, no en una box de bot.

## Conectores

MCP con la cuenta del usuario. Después de conectar, una lectura que identifique a quién pertenece esa fuente, como
pide `quarry`. «Conectado» no alcanza. No se verificó ninguna cuenta al escribir este archivo.

## Checklist de prueba

Nada de esta lista se hizo. Marcar «probado» en el contrato pide un uso real.

- [ ] El bot carga `foreman` (por skill o por el índice) y arma el plan de un pedido de dos fases.
- [ ] Lee un `SKILL.md` por ruta y sigue un paso.
- [ ] La primera respuesta avisa en una línea si el buzón tiene ideas nuevas.
- [ ] Una ficha de `tokenwise` termina en un solo `executor`, reutilizado con `MessageSubagent`, sin un segundo
      `Task` en el mismo workstream.
- [ ] Un segundo `computerUse` no arranca mientras hay uno activo.
- [ ] `python foundry/scripts/auditar_gremio.py` corre en la box sin `machineId`.
- [ ] Antes de leer un conector, se verifica la identidad de esa cuenta.
- [ ] Una escritura afuera queda en `DraftExternalMessage` hasta un sí explícito.
- [ ] Una `UpdateRoutine` de `sherpa` dispara sola y no escribe en otra parte sin la autorización permanente acotada.
- [ ] Una `UpdateRoutine` corre `python foundry/scripts/auditar_gremio.py --dinamico --al-buzon` y deja propuestas
      en el buzón, sin editar skills y sin leer sesiones.
