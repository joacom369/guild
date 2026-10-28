# Auditoría del adaptador Grok Bot

Fecha: 2026-10-28. Alcance: diseño del adaptador y corrida local del harness. No es una prueba del bot: ninguna fila del
contrato pasó a «probado».

El texto que manda para Grok Bot es [`adaptadores/grok-bot.md`](../adaptadores/grok-bot.md). Este informe dice qué se
vio al recorrer los oficios y qué se corrió.

## Cómo se corrió

En la máquina donde se escribió el adaptador (no en una box de Grok Bot). `python` no estaba en el PATH; se usó
`python3`. Misma biblioteca estándar.

```bash
python3 foundry/scripts/auditar_gremio.py --autoprueba
python3 foundry/scripts/auditar_gremio.py
```

La autoprueba salió bien: los detectores vieron un gremio sembrado con caso negativo ausente, piso ausente, solape de
momento, regla duplicada, dueño repetido, dueño inexistente, skill fuera del índice y enlace roto. `ponytail`, que
está en la lista de oficios externos, no se marcó como aviso.

La corrida sobre el repo salió 0 (hay avisos; no hay errores). Salida completa:

```
Auditoría del gremio
Raíz: /workspace
Skills leídas: 14 (assay, compass, design-taste-frontend, foreman, foundry, hallmark, herald, impeccable, kiln, lenses, provenance, quarry, sherpa, tokenwise)
Resumen: caso negativo: 0 error; piso: 0 error; robo de momento: 5 aviso, 5 info; reglas duplicadas: 3; dueños: 1; índice: 0

## dueño
[info] dueño: ponytail
    oficio externo: la tabla §3 lo nombra dueño de «Código mínimo» y no vive en este repositorio

## regla duplicada
[aviso] regla duplicada: foundry × lenses (74%)
    «agrega una fila en el registro de automatizaciones que fija la configuracion del ambiente por defecto»
    «una fila por propuesta en el registro de lentes que fija la configuracion del ambiente»

[aviso] regla duplicada: hallmark × tokenwise (74%)
    «el proyecto ya tiene pruebas o un control de paridad se corren y su resultado se informa tal como salio»
    «si el proyecto tiene pruebas o un control de paridad se corren antes de dar»

[aviso] regla duplicada: herald × lenses (81%)
    «registrar en el registro de escrituras que fija la configuracion del ambiente»
    «una fila por propuesta en el registro de lentes que fija la configuracion del ambiente»

## robo de momento
[aviso] robo de momento: compass × impeccable
    ninguno nombra al otro en el caso negativo (una en el «Usar…» y la otra en el preámbulo). Palabras: dashboards

[aviso] robo de momento: foundry × lenses
    ninguno nombra al otro en el caso negativo (una en el «Usar…» y la otra en el preámbulo). Palabras: automatizacion, creativo, esceptico, innovador, meticuloso, opciones, optimista, separado

[aviso] robo de momento: hallmark × herald
    ninguno nombra al otro en el caso negativo (una en el «Usar…» y la otra en el preámbulo). Palabras: publicar

[aviso] robo de momento: impeccable × kiln
    ninguno nombra al otro en el caso negativo (en el «Usar…»). Palabras: dashboard, frontend, landing

[aviso] robo de momento: kiln × quarry
    ninguno nombra al otro en el caso negativo (una en el «Usar…» y la otra en el preámbulo). Palabras: pagina, planilla

[info] robo de momento: assay × compass
    el caso negativo ya nombra al otro (en el «Usar…»). Palabras: analisis, aplica, indicador, tecnica

[info] robo de momento: assay × provenance
    el caso negativo ya nombra al otro (una en el «Usar…» y la otra en el preámbulo). Palabras: analisis, conclusion, evaluacion, sensibilidad

[info] robo de momento: compass × provenance
    el caso negativo ya nombra al otro (en el «Usar…»). Palabras: analisis, ciencia, cifra, espacial, supuesto

[info] robo de momento: design-taste-frontend
    disable-model-invocation: no compite por el disparo; se carga sólo por nombre

[info] robo de momento: hallmark × kiln
    el caso negativo ya nombra al otro (una en el «Usar…» y la otra en el preámbulo). Palabras: informe, planilla, presentacion, tablero

Lectura: un error es una skill propia sin caso negativo o sin piso. Un aviso es una pista (solape o texto casi igual). Un info es un solape que el caso negativo ya cubre, una skill que sólo se carga por nombre, o un dueño externo que el mapa ya nombra. Las tasas de disparo las controla empaquetar.py.
```

El script vive en `foundry/scripts/` porque `foundry` es el dueño de cómo se escribe una skill y del piso. `assay`
sigue con las corridas de datos. No se editaron oficios para que encajen en Grok Bot: en `foreman` y en `tokenwise`
hay un puntero de dos líneas al adaptador de la plataforma, sin nombrar a Grok Bot y sin copiar sus límites.

## Solapes y riesgos, leídos

Los avisos no se corrigieron en los oficios. Cambiar una description es decisión del usuario (regla 5 de `foreman`)
y, si se hace, pide pruebas de disparo. Quedan anotados para el buzón.

| Hallazgo | Lectura |
|---|---|
| `foundry` × `lenses` | El preámbulo de `foundry` nombra las siete lentes. El caso negativo nombra a `foreman`, no a `lenses`. El cuerpo ya dice convocar a `lenses`. Es el solape más concreto: «¿qué diría un escéptico?» puede cargar los dos. |
| `impeccable` × `kiln`, y `compass` × `impeccable` por «dashboards» | El momento visual (landing, dashboard, frontend) lo comparten `kiln` y la skill de terceros. El caso negativo de `kiln` nombra a `compass` y a `hallmark`, no a `impeccable`. `design-taste-frontend` no compite: sólo se carga por nombre. |
| `hallmark` × `herald` por «publicar» | «Publicar algo con números» y «publicá» no se excluyen entre sí. Un pedido de publicar un informe puede cargar los dos. |
| `kiln` × `quarry` por «página» y «planilla» | Está en el preámbulo, no en el «Usar…». En `AGENTS.md` los momentos siguen distintos (construir un entregable / sacar datos). Pista débil. |
| Registros del ambiente (`foundry`, `lenses`, `herald`, 74–81 %) | La misma frase de «el registro que fija la configuración del ambiente». El dueño de dónde vive esa configuración es `foreman` (`referencias/ambiente-ejemplo.md`). Son la instrucción local de cada registro, no dos dueños de una regla. |
| `hallmark` × `tokenwise` (74 %) | La frase del control de paridad. El mapa ya dejaba abiertas las repeticiones menores entre `provenance`, `hallmark`, `tokenwise` y `assay` sobre cómo se verifica. El dueño del procedimiento de verificación es `hallmark`. |
| `ponytail` | Info. El mapa lo nombra dueño de «código mínimo» y el oficio no está en este repo. Entra en la lista de externos del script para no tratarlo como un dueño fantasma. |

Lo que el harness no marcó y igual conviene tener a la vista:

- La description de `foreman` dice que despliega las lentes en puntos fijos. Comparte con `lenses` una palabra corta
  y el script no la sube a aviso. El caso negativo de `foreman` nombra a la skill de la fase y a `foundry`, no a
  `lenses`.
- «Tablero» está en el «Usar…» de `kiln` y en el preámbulo de `compass` y de `hallmark`. `hallmark` × `kiln` sale
  como info porque el caso negativo ya nombra a `kiln`. `compass` también nombra a `kiln` en el suyo.
- El índice de `AGENTS.md` no tuvo solapes por encima del corte (0 avisos). Para Grok Bot importa: cuando no hay
  descriptions nativas, el bot se guía por ese índice, que está más separado que las descriptions.

Las descriptions de las 12 skills propias siguen con caso negativo que nombra a otro oficio, y las 12 tienen
`evals/piso.json`. Las huellas de esas descriptions coinciden con el piso: este cambio no las tocó.

## Qué detecta el harness y qué sigue a mano

| Solo | A mano |
|---|---|
| Falta el caso negativo, o niega sin nombrar al dueño | Si ese caso negativo alcanza cuando las dos skills están cargadas |
| Palabras compartidas del «Usar…» y anclas raras del preámbulo | Si ese solape roba el momento de verdad. `claude plugin eval` no carga dos skills a la vez |
| Enunciado casi igual, o una ventana de palabras idéntica | Si es una regla copiada o la misma plantilla (el registro del ambiente) |
| Falta `evals/piso.json` en una skill propia | Las tasas, y que el piso no baje: `empaquetar.py` |
| Dos filas de `MAPA.md` §3 con la misma regla, o un dueño que no existe | Si un oficio externo (`ponytail`) tiene que entrar al repo |
| `AGENTS.md`: enlace roto, skill fuera de la tabla, momentos con las mismas palabras | Si el índice, leído por una persona, sigue siendo claro |
| — | El checklist de `adaptadores/grok-bot.md`. Nada de eso se marcó hecho |
| — | Qué hay instalado en una box de Grok Bot (Chrome, `websockets`, `openpyxl`) |

## Cómo no se pisan los agentes

El detalle y el motivo están en la sección «Reglas anti-pisado» de
[`adaptadores/grok-bot.md`](../adaptadores/grok-bot.md). Resumen para esta plataforma:

- Un dueño por fase: lo decide `foreman`. Un `executor` no rearma el plan.
- Un workstream, un `executor`, reutilizado con `MessageSubagent`. Otro `Task` es otro trabajo o un fan-out.
- El fan-out (varios `Task` a la vez) espera el permiso del usuario. El pedido es la ficha de `tokenwise` §2; dentro
  de un trabajo lo aprueba `foreman` (regla 3).
- `computerUse` de a uno. Tope blando de unos cuatro `executor`; es de la plataforma, no se midió acá, y no es un
  tope de tokens.
- Un escritor por archivo: la regla es de `tokenwise` §1.
- Escribir afuera pasa por `herald`: borrador con `DraftExternalMessage`, envío sólo con el sí de esa acción. Un
  subagente no envía.
- El código de un repositorio va a CloudAgent. No se clona el repo en la box del bot para editarlo.

## Qué no se verificó

- No se pegó el índice en un perfil, no se lanzó un `Task`, no se creó una `UpdateRoutine` y no se armó un
  `DraftExternalMessage`.
- No se comprobó la identidad de ningún conector.
- No se regeneró `docs/mapa.png`. El diagrama no cambió; en `mapa/mapa.html` se actualizó el párrafo de adaptadores
  y la línea de «qué falta».
- Las pruebas de disparo no se volvieron a correr: las descriptions no cambiaron.
