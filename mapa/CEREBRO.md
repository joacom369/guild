# foreman y foundry · el cerebro y el taller · borrador (2026-10-25)

Nada de esto está construido. Es la estructura que surge de la charla y la auditoría, con las decisiones abiertas al
final.

## Dos piezas, no una

| Pieza | Qué es | Cuándo actúa |
|---|---|---|
| **Cerebro** (la mano derecha) | Conoce el árbol, deriva cada pedido a la skill que corresponde, habla con el usuario sólo cuando vale la pena y guarda ideas de mejora | Siempre, en segundo plano |
| **Taller** (la fábrica de automatizaciones) | Convierte «estoy repitiendo esta tarea» en una automatización: la releva, decide si vale la pena, busca en el árbol, propone opciones y construye la elegida | Cuando el usuario lo pide, o cuando el cerebro detecta una repetición y lo propone |

Separarlas evita que el cerebro se vuelva un todopoderoso: **el cerebro decide quién trabaja; el taller agrega ramas
al árbol**. Cada automatización nueva es un nodo más, y así se corre la curva de productividad.

## El taller, paso a paso

1. **Relevar la tarea.** Cada cuánto se repite, cuánto lleva, qué entra y qué sale, qué sistemas toca, qué decide una
   persona y qué pasa si sale mal.
2. **¿Vale la pena?** El tiempo que ahorra (frecuencia × duración × horizonte) contra el costo de construirla y
   mantenerla, más el riesgo de que falle sin que nadie lo note. Si no vale la pena, se dice.
3. **Buscar en el árbol.** Qué pasos ya resuelve una skill, un script o un agente que existe. No se construye lo que
   ya está.
4. **Las lentes proponen, cada una por separado** (sin debate entre ellas; ver más abajo).
5. **El cerebro sintetiza** dos o tres opciones con su costo, su riesgo y lo que exigen. **Decide el usuario.**
6. **Construir y probar** con las skills de cada fase: `ponytail` para el código, `hallmark` para el control y
   `claude plugin eval` para el disparo.
7. **Registrar en el mapa** el nodo nuevo, con su dueño, su entrada y su salida, y **una predicción refutable**:
   «ahorra X horas por mes». Después de N usos se mide si se cumplió.

### La escalera de automatización (de menos a más autonomía y costo)

| Escalón | Mecanismo | Sirve cuando |
|---|---|---|
| 1 | Una regla o lista de pasos en CLAUDE.md | La tarea es corta y basta con no olvidarse |
| 2 | Una skill | Hay un procedimiento con criterio |
| 3 | Un script | Hay pasos mecánicos que tienen que dar siempre lo mismo |
| 4 | Un subagente definido (`.claude/agents/`) | Una parte lee mucho material o necesita aislarse |
| 5 | Un hook | Algo tiene que pasar sí o sí en un evento |
| 6 | Un workflow | Varios agentes con verificación cruzada, siempre en el mismo orden |
| 7 | Una rutina programada | La tarea corre sola, sin que el usuario la pida |

La lente vaga empuja hacia abajo en la escalera; la optimista, hacia arriba.

## Las lentes (las «personalidades»)

Cada lente tiene un nombre y un carácter, pero trabaja con un **contrato**: qué produce y con qué criterio. Así
conserva lo que se busca de la personalidad y respeta la regla de `tokenwise` («qué hacer, no quién ser»). Varias ya
existen como skill:

| Lente | Pregunta que la mueve | Qué produce | Se apoya en |
|---|---|---|---|
| **El vago** | ¿Qué es lo mínimo que llega al resultado? | La opción más barata, con lo que se pierde | `ponytail` |
| **El optimista** | ¿Qué pasa si sale todo bien y lo llevamos al máximo? | El techo, rotulado como techo, y qué tendría que ser cierto para llegar | `provenance` (el techo se rotula) |
| **El meticuloso** | ¿Qué se puede romper y cómo nos enteramos? | Los controles, los casos límite y el acta | `hallmark` |
| **El escéptico** *(propuesta)* | ¿Vale la pena? ¿Contra qué se compara? | El costo, el contrafáctico y el umbral | `provenance`, `compass` |
| **El curioso** *(el cerebro mismo)* | ¿Qué se podría hacer mejor o distinto? | Ideas para la posdata o el buzón | — |

Según la evidencia (AUDITORIA.md), las lentes rinden cuando **proponen por separado y alguien sintetiza**, no cuando
debaten hasta coincidir.

## El cerebro como mano derecha

- **Habla cuando vale la pena.** Interrumpe sólo por:
  - un riesgo,
  - una decisión que es del usuario,
  - una repetición que el taller podría automatizar.
  El resto va en la **posdata rotulada** al final de la respuesta, que ya es una regla de `provenance`.
- **Curiosidad con buzón.** Las ideas de mejora (herramientas, áreas, skills) se anotan en un buzón (`IDEAS.md`) en
  lugar de soltarse en medio de una tarea. Cuando el usuario pide charlar, el cerebro abre el buzón.
- **Despliegue a pedido.** El usuario decide cuánto se despliega del árbol. Modos posibles:
  - sólo conversación;
  - propone y espera;
  - ejecuta un tramo con cortes en puntos fijos.

## Decisiones tomadas (2026-10-25)

1. **Dos piezas:** cerebro y taller.
2. **Laboratorio de lentes:** siete lentes aprobadas (vago, optimista, creativo, meticuloso, escéptico, innovador,
   lector). Están para abrir la cabeza; algunas propuestas van a sobrar y eso es parte de aprender. El cerebro anota
   qué lente aportó qué, para ver con el tiempo cuáles rinden en cada punto.
3. **Curiosidad:** las ideas van a un buzón versionado (`mapa/IDEAS.md`), cada una con fecha, área y por qué
   importa. Al empezar una conversación, el cerebro avisa en **una línea** si hay ideas nuevas («Hay 3 ideas nuevas
   en el buzón; ¿las charlamos?»). Nunca interrumpe una tarea por una idea.
4. **Detección de repeticiones:** el cerebro las detecta y propone llevarlas al taller. Antes de mirar, consulta al
   usuario qué va a leer y cuánto va a gastar. Con el visto bueno tiene vía libre para leer y proponer; nunca
   modifica nada sin consentimiento.
5. **Nombres:** el cerebro es **`foreman`** (el capataz: conoce cada oficio, decide quién entra y habla con el
   dueño) y el taller es **`foundry`** (la fundición: hace el molde para una tarea que se repite).

## Principio: un núcleo que se lleva a cualquier plataforma

El objetivo es levantar el árbol en cualquier plataforma (Cursor, un bot en servidor propio como Grok Bot u otra), no sólo en Claude. Por
eso el sistema se arma en dos capas:

| Capa | Qué tiene | Se lleva tal cual |
|---|---|---|
| **Núcleo** | El mapa, los SKILL.md (texto), los contratos de entrada y salida, las lentes y los scripts en Python | Sí: es texto y Python |
| **Adaptadores** | Lo propio de cada plataforma: en Claude Code, hooks, `.claude/agents/`, workflows y rutinas; en otras, `AGENTS.md`, sus reglas y sus agentes | No: uno por plataforma |

Regla: **nada del núcleo depende de una plataforma.** Si una skill necesita un hook o un agente, lo dice como
necesidad («al empezar la sesión, leer el buzón») y cada adaptador lo resuelve a su manera. El contrato que
tiene que cumplir cada adaptador está en `MAPA.md` §6; antes de escribir uno hay que verificar qué soporta hoy la
plataforma.

## Más adelante (anotado, no se diseña todavía)

- Arranque completo del árbol: el usuario lo levanta y el sistema empieza a trabajar y a desplegar agentes solo.
- Agentes desplegados con nombres fáciles de recordar, que digan qué están haciendo (pueden ser los de las skills).
- Traslado de información entre agentes y plataformas.
