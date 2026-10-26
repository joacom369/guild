# Guild: índice para cualquier agente

Este repositorio es un sistema de trabajo: cada carpeta es un **oficio** con su procedimiento en `SKILL.md`. Si tu
plataforma no carga skills sola, usá este índice: cuando la tarea coincide con un momento de la tabla, **leé el
`SKILL.md` de ese oficio antes de seguir y aplicalo**, incluidas sus `referencias/` cuando el texto lo pida.

## Para qué

Que el usuario reciba un trabajo excelente sin tener que rehacerlo ni controlarlo pieza por pieza: cada cifra con su
origen, cada entrega con su acta, cada decisión de método tomada por el usuario. La cosmovisión completa está en
[`foreman/SKILL.md`](foreman/SKILL.md).

## Lo que no se negocia

Cada regla tiene un solo dueño y acá no se copia:
- los cortes en los que se consulta al usuario son la regla 2 de [`foreman/SKILL.md`](foreman/SKILL.md);
- toda escritura afuera, o borrar algo del usuario, pasa por [`herald/SKILL.md`](herald/SKILL.md);
- un oficio que necesita agentes los pide con la ficha de [`tokenwise/SKILL.md`](tokenwise/SKILL.md) §2.

Las reglas del ambiente (el archivo de reglas del proyecto o del usuario) y sus skills de dominio mandan sobre este
repositorio.

## Qué oficio y cuándo

| Momento | Oficio | Leer |
|---|---|---|
| Empezar, retomar o cerrar un proyecto o un trabajo de varios pasos | `foreman` (el capataz) | [`foreman/SKILL.md`](foreman/SKILL.md) |
| Plantear un trabajo con datos, interpretar un resultado, antes de concluir | `provenance` | [`provenance/SKILL.md`](provenance/SKILL.md) |
| Elegir una técnica o herramienta, o decidir si hace falta | `compass` | [`compass/SKILL.md`](compass/SKILL.md) |
| Pedir agentes para una tarea, elegir modelo, cuidar el costo | `tokenwise` | [`tokenwise/SKILL.md`](tokenwise/SKILL.md) |
| Abrir opciones desde siete ángulos antes de una decisión grande | `lenses` | [`lenses/SKILL.md`](lenses/SKILL.md) |
| Sacar datos de cualquier origen | `quarry` | [`quarry/SKILL.md`](quarry/SKILL.md) |
| Calcular, modelar, pronosticar, comparar | `assay` | [`assay/SKILL.md`](assay/SKILL.md) |
| Construir un entregable: página, tablero, documento, planilla, presentación | `kiln` | [`kiln/SKILL.md`](kiln/SKILL.md) |
| Controlar un entregable con cifras antes de darlo | `hallmark` | [`hallmark/SKILL.md`](hallmark/SKILL.md) |
| Escribir afuera (responder, publicar, cambiar un estado) o borrar algo | `herald` | [`herald/SKILL.md`](herald/SKILL.md) |
| Una tarea que se repite y se quiere automatizar | `foundry` | [`foundry/SKILL.md`](foundry/SKILL.md) |
| Ponerse al día con las fuentes conectadas (chat, correo, calendario u otras) | `sherpa` | [`sherpa/SKILL.md`](sherpa/SKILL.md) |
| Pulir o auditar una interfaz | `impeccable` (de terceros) | [`impeccable/SKILL.md`](impeccable/SKILL.md) |
| Dirección visual sin aspecto de plantilla | `design-taste-frontend` (de terceros) | [`design-taste-frontend/SKILL.md`](design-taste-frontend/SKILL.md) |

Un pedido de una sola fase va directo a su oficio; un trabajo de varias fases empieza por `foreman`, que arma el plan
con la tabla de [`foreman/referencias/ciclo.md`](foreman/referencias/ciclo.md).

## Herramientas

Los scripts de cada oficio (`<oficio>/scripts/`) son Python con la biblioteca estándar (más `openpyxl` para `.xlsx`, y
Chrome con `websockets` para las capturas de `kiln`) y corren igual en cualquier plataforma. Las rutas de los `SKILL.md` son relativas a esta carpeta.

## Lo propio de la plataforma

Lo que cada plataforma tiene que darle al sistema (cargar oficios, reglas, inicio de sesión, agentes, rutinas,
conectores) está en el contrato del adaptador: [`mapa/MAPA.md`](mapa/MAPA.md) §6, y el detalle de cada plataforma en
[`adaptadores/`](adaptadores/).
