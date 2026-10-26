# El ciclo de un trabajo

`foreman` es el dueño de esta tabla. El mapa del sistema la resume y apunta acá.

## Las siete fases

| Fase | Skill dueña | Recibe | Entrega | Corte con el usuario |
|---|---|---|---|---|
| 1 Plantear | `provenance` | El pedido | Pregunta de análisis y alcance (describe, explica o evalúa); qué es variable, parámetro o supuesto | Si la lectura del pedido cambia lo que se hace |
| 2 Decidir método | `compass` + `tokenwise` | La pregunta | Veredicto de técnica (aplica, no aplica, todavía no) y plan de trabajo con su costo | **Siempre**: el método lo decide el usuario |
| 3 Extraer | `quarry` | Qué datos y de dónde | Carpeta con la foto, `FICHA.json` y el perfil | Antes de una extracción grande |
| 4 Analizar | `assay` (con los axiomas de `provenance`) | Foto verificada y veredicto | Carpeta de corrida con `CORRIDA.json`, intentos contados | Si un supuesto cae o el diagnóstico falla |
| 5 Construir | `kiln` · `dataviz` · `ponytail` | Las salidas | El entregable (página, informe, planilla) | En la dirección visual |
| 6 Verificar | `hallmark` | Entregable y salidas | Acta: sale, sale con observaciones o no sale | Si no sale: entregar igual lo decide el usuario |
| 7 Registrar | `provenance` (plantillas) + `foreman` | Acta y decisiones | ESTADO.md actualizado y la entrega (conclusión, opciones, lo que no se sabe) | — |

## Qué fases aplican según la tarea

| Tipo de tarea | Fases | Ejemplo |
|---|---|---|
| Análisis con cifras que sostienen una decisión | 1 a 7 | Evaluar una inversión, un informe de resultados |
| Página o tablero sin cifras propias | 1, 5 y la lectura de la 6 | Landing, rediseño |
| Página o tablero con cifras | 1, 2 (¿hace falta?), 3 si hay que sacar datos, 4, 5, 6 completa | Tablero comercial |
| Investigación o relevamiento | 1, 2 (`tokenwise` si se reparte), 3, 6, 7 | Relevar proveedores de un país |
| Cambio de código | `ponytail` + las pruebas del proyecto | Arreglar un error |
| Consulta rápida | Se contesta directo, sin plan | Una definición, un dato con su fuente |
| Tarea que se repite | `foundry` | «Todos los lunes armo este reporte» |
| Migrar o integrar un sistema | `quarry` (copia con ficha) → port con paridad contra el original (`ponytail` + 6) → cortar la dependencia | Pasar un proyecto a otra herramienta |
| Conectar una fuente o herramienta | Identidad, permiso mínimo, una lectura real de prueba y el registro en la configuración (`sherpa/referencias/conectores.md`) | Conectar el chat o el correo propios |
| Ponerse al día con el chat y el correo | `sherpa` | «¿Qué me perdí?» |

Si el tipo no está en la tabla, se elige el más parecido y se dice cuál se eligió. Si aparece seguido, se propone
sumarlo a esta tabla (va al buzón).

## Retornos

Si `hallmark` dice «no sale», se vuelve a la fase dueña del error:
- una cifra mal calculada vuelve a la 4;
- un dato mal extraído, a la 3;
- un texto mal copiado o un gráfico mal armado, a la 5;
- una conclusión que no se sostiene, a la 1 o la 2.
