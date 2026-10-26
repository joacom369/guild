---
name: foundry
description: Taller que convierte una tarea que se repite en una automatización. Releva la tarea, calcula si vale la pena (tiempo ahorrado contra costo de construir y mantener), busca qué partes ya resuelven las skills y herramientas instaladas, hace que varias lentes propongan por separado (vago, optimista, creativo, meticuloso, escéptico, innovador, lector), presenta dos o tres opciones con su costo y riesgo, construye la que elige el usuario y la registra en el mapa con una predicción que se mide. Usar cuando el usuario dice que repite una tarea, «todos los días hago…», «esto se podría automatizar», «quiero delegar esto en un agente», o con /foundry. No ejecuta la tarea en sí (eso lo hace la automatización que sale de acá) ni decide cuál skill trabaja en cada momento (`foreman`).
argument-hint: "[la tarea que se repite]"
---

# Foundry: el molde para lo que se repite

En una fundición no se tallan piezas de a una: se hace un molde y el molde produce la serie. Esta skill no hace la
tarea repetida; **hace el molde**. Cada molde nuevo es una rama más del árbol de skills, y así se corre la curva de
productividad: lo que hoy cuesta una hora por día pasa a costar unos minutos de revisión.

## Las reglas (no se negocian)

1. **Las decisiones son del usuario.** Esta skill releva, calcula y propone; qué se construye y con cuánta autonomía
   lo decide él.
2. **Sin permiso, nada se escribe en sistemas ajenos.** Una automatización que lee de un sistema (Slack, correo, una
   base) no publica, no responde, no marca como leído ni borra nada salvo que el usuario lo pida explícitamente para
   ese paso. Las reglas del ambiente mandan.
3. **No se construye lo que ya existe.** Antes de diseñar, se busca en el árbol.
4. **Toda automatización nace con su control.** Si nadie se entera cuando falla, no está terminada.
5. **Se mide lo que se prometió.** La predicción de ahorro se registra y se compara después con lo que pasó.

## El procedimiento

### 1. Relevar la tarea

Preguntá sólo lo que no se puede averiguar; con `AskUserQuestion` si está disponible. Lo que hace falta saber:

| Qué | Por qué importa |
|---|---|
| **Frecuencia y duración**: cada cuánto y cuánto lleva cada vez | Es el ahorro posible |
| **Entrada**: de dónde sale la información (sistema, canal, archivo) y cuánta es | Define qué hay que leer y con qué permisos |
| **Criterio**: qué hace la persona con cada ítem (lo descarta, lo lee, actúa, delega) y cómo decide | Es lo difícil de automatizar; si no se puede escribir, la automatización sólo asiste |
| **Salida**: qué tiene que quedar al final (un resumen, una lista de pendientes, respuestas, un registro) | Es el contrato de la automatización |
| **Riesgo**: qué pasa si se escapa algo o se clasifica mal | Fija cuánto control hace falta |
| **Cuándo y dónde**: a qué hora hace falta el resultado y dónde lo quiere ver | Define el mecanismo (a pedido, programado) |

Si el ambiente tiene una **plantilla propia para escribir el conocimiento de un área** (por ejemplo, una skill de
dominio que pregunta decisiones, fuentes, alarmas, quién es quién y vocabulario), usala acá: sus «alarmas» son el
criterio de qué es urgente, que es lo más difícil de automatizar.

Cerrá el relevamiento en un párrafo: «La tarea es…, entra…, el criterio es…, sale…, el riesgo es…». El usuario lo
confirma o lo corrige antes de seguir.

### 2. ¿Vale la pena?

```
ahorro por mes = frecuencia por mes × (minutos hoy − minutos con la automatización)
costo          = horas de construir + horas de mantener por mes + costo de uso (tokens, herramientas)
recupero       = costo de construir ÷ (ahorro por mes − mantener por mes)
```

Cada número lleva su naturaleza: los minutos de hoy los dice el usuario (observado o estimado por él); los minutos
con la automatización son un **supuesto** hasta medirlos. Mostrá también el **riesgo de error silencioso**: una
automatización que ahorra 30 minutos pero deja pasar un mensaje urgente puede costar más de lo que ahorra.

Si no vale la pena, decilo con la cuenta. A veces la mejor salida es un escalón bajo (una regla, una checklist).

### 3. Buscar en el árbol

Recorré la lista de skills disponibles, los conectores (MCP), los scripts instalados y, si el ambiente tiene una
**base de conocimiento** separada de las skills (un repositorio de conceptos con dueño y fecha), también esa base.
Armá una tabla:

| Paso de la tarea | ¿Quién lo resuelve hoy? | Qué falta |
|---|---|---|

Se reusa lo que hay, aunque sea de otro dominio: una skill que clasifica correos es un buen molde para clasificar
mensajes de chat. Lo que falta es lo único que se construye.

### 4. Las lentes proponen

Convocá las lentes con la skill `lenses`, en su punto «diseñar una automatización»: por defecto vago, optimista,
escéptico y meticuloso; el creativo, el innovador y el lector se suman cuando la tarea es nueva para el árbol o cuando
su resultado lo usa otra persona. Los contratos, cómo se proponen y el registro son de `lenses`. Si no está
instalada, cada lente responde su pregunta en un bloque aparte: vago (lo mínimo que llega), optimista (el techo),
escéptico (¿vale la pena?), meticuloso (qué se rompe).

Anotá qué lente propuso qué: al final se registra cuál terminó usándose.

### 5. Sintetizar y decidir

Con las propuestas, armá **dos o tres opciones** en la escalera de automatización:

| Escalón | Mecanismo | Sirve cuando |
|---|---|---|
| 1 | Una regla o una checklist en el archivo de reglas | Basta con no olvidarse de un paso |
| 2 | Una skill | Hay un procedimiento con criterio que se pide a demanda |
| 3 | Un script | Hay pasos mecánicos que tienen que dar siempre lo mismo |
| 4 | Un subagente definido | Una parte lee mucho material o necesita aislarse |
| 5 | Un hook | Algo tiene que pasar sí o sí en un evento |
| 6 | Un workflow | Varios agentes en un orden fijo, con verificación cruzada |
| 7 | Una rutina programada | La tarea corre sola, sin que el usuario la pida |

Cada opción, en una tabla: qué hace, en qué escalón, ahorro estimado, costo, riesgo principal, qué control trae y
qué lente la propuso. Recomendá una y decí por qué; **decide el usuario**. Una opción baja y que se pueda subir de
escalón después suele ser mejor que una alta de entrada.

### 6. Construir y probar

Con las skills de cada fase: `ponytail` para el código, `quarry` si hay que sacar datos, `kiln` si la salida es una
página, `hallmark` para el control. La primera corrida se hace **con el usuario mirando**, contra el método manual del
mismo día: lo que la automatización dejó afuera y la persona no, es el primer ajuste. Si la automatización es una skill, se escribe con [referencias/escribir-skills.md](referencias/escribir-skills.md). Si la automatización es una
skill, se prueba su disparo (`claude plugin eval`, si está disponible).

### 7. Registrar

Agregá una fila en el registro de automatizaciones que fija la configuración del ambiente (por defecto,
`~/.foreman/AUTOMATIZACIONES.md`), y creá el archivo si no existe:

```markdown
| Fecha | Automatización | Escalón | Tarea que reemplaza | Predicción (fechada) | Lentes que aportaron | Medición |
|---|---|---|---|---|---|---|
| 2026-10-25 | <nombre> | 7 rutina | Revisar Slack a mano | Ahorra 25 min/día; ningún pendiente urgente perdido en 4 semanas | vago (base), meticuloso (control) | pendiente: 2026-11-22 |
```

En la fecha de medición, se compara la predicción con lo que pasó, y lo que se aprendió vuelve a esta skill o a las
lentes.

## Cómo se combina

- `foreman` detecta tareas repetidas y las trae acá, y mira las mediciones vencidas al abrir.
- `lenses` en el paso 4.
- `tokenwise` cuando las lentes o la construcción van con agentes (el pedido de delegación).
- `herald` si la automatización escribe afuera.
- `provenance` para la cuenta de si vale la pena (cada número con su naturaleza).
- `ponytail`, `quarry`, `kiln` y `hallmark` para construir y controlar.
