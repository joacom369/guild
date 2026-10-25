# Modelo principal y asesor (advisor): el detalle

Los nombres de modelos y las condiciones de costo cambian: verificá contra la documentación vigente antes de
recomendar una combinación.

Claude Code puede sumar un **asesor**: un segundo modelo, más fuerte, que Claude consulta en los puntos de decisión
(antes de elegir un enfoque, ante un error que se repite, antes de dar algo por terminado). Lee la conversación entera y
devuelve una recomendación. Se activa con `/advisor <modelo>`, se apaga con `/advisor off` y lo decide el usuario: es su
configuración y su cuota.

**Cuándo conviene:**
- Tareas largas y de varios pasos, donde casi todo es rutina pero el plan decide el resultado: extracción y modelo de
  datos, refactors grandes, errores que vuelven.
- Cuando se quiere un control independiente antes de cerrar algo importante.

**Cuándo no:**
- Tareas cortas: la consulta cuesta más de lo que aporta.
- Sesiones muy largas. Cada consulta procesa la conversación completa sin caché, así que en una sesión de horas cada
  consulta es cara. Es mejor activarlo en una sesión nueva.

**Combinaciones de partida (el asesor debe ser igual o más fuerte que el principal):**

| Trabajo | Principal | Asesor | Por qué |
|---|---|---|---|
| Rutina con decisiones clave (extraer, convertir, controlar, programar) | Sonnet | Opus | Más barato que correr Opus todo el tiempo; la calidad se cuida en los puntos de decisión |
| Método, teoría, diseño de indicadores, decisiones con el usuario | Opus | ninguno | El razonamiento ya está en el principal |
| Tarea de alto riesgo donde importa una segunda mirada | Opus | Opus o Fable | Control independiente; caro, y Fable consume créditos aparte |

La tabla es un punto de partida, no una regla: con más margen de uso, el principal fuerte en todo el trabajo puede valer
la pena. Lo decide el usuario.

**Relación con los agentes críticos:**
- El asesor revisa decisiones en el momento y con todo el contexto.
- El agente crítico revisa un resultado terminado, sin ver el plan y con una lectura dirigida.
- No se duplican: la auditoría grande de una ronda sigue siendo un crítico; el asesor cuida el camino.

Lo que dice el asesor es una opinión, no una instrucción: si choca con la evidencia (un archivo, una prueba, una cifra
controlada), se le muestra el conflicto al usuario en lugar de seguirlo.
