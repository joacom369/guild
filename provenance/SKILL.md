---
name: provenance
description: Forma de pensar para trabajos con datos, modelos, evaluaciones, investigaciones o decisiones (tesis, informes, análisis económicos y financieros, proyectos de inversión, ciencia de datos, análisis espacial). Axiomas sobre el origen y la naturaleza de cada cifra, nivel de cada conclusión, validación contra la propia ilusión y hábitos para no casarse con un supuesto. Usar al plantear un trabajo analítico, al interpretar un resultado y antes de concluir, o cuando el usuario pide rigor, metodología, sensibilidad o crítica. No es el procedimiento para sacar datos de un sistema ni para guardar su procedencia, con consulta, ficha y hash (eso es `quarry`), ni para elegir una técnica (`compass`), analizar (`assay`) ni controlar un entregable antes de darlo (`hallmark`). También con /provenance.
---

# Método riguroso: cada cifra con su origen, cada conclusión con su nivel

Sirve para cualquier trabajo donde números o afirmaciones sostengan una
decisión. Ordena el criterio del usuario; no lo reemplaza. **Las decisiones son
del usuario**: tu tarea es mostrarle las opciones, sus consecuencias y lo que no
se sabe. Rigor sin rigidez: el método se ajusta cuando cruje, y se anota dónde.

## Los axiomas (no se negocian)

1. **Ninguna cifra nace en la presentación.** Todo número del texto, la tabla o
   la pantalla sale de un cálculo reproducible y se copia de su salida, nunca de
   memoria: un comentario que dice 0,587 y un texto que dice 0,52 es el error
   típico.
2. **Un dato ausente nunca es cero.** «No sé» y «no hay» son afirmaciones
   distintas, y «cero registros en esta copia» no es «no existe en el mundo».
   Lo que falta se deja vacío, con su estado y con lo que haría falta. Un cero
   vale sólo si es un resultado.
3. **No hay conclusión con insumos vacíos ni con supuestos caídos, y cada
   conclusión lleva su nivel.** Si el diagnóstico del modelo falla, la
   conclusión correcta es «no concluyo», con lo que haría falta para concluir.
   El nivel:
   *preliminar sobre referencias* si alguna pieza descansa en un valor público o
   un supuesto, *definitivo* si todas descansan en datos propios o
   cotizaciones firmes. Un techo («si todo sale bien») se rotula como techo.
4. **Cada cifra declara su naturaleza** (este es el vocabulario único; las demás skills lo usan tal cual): observado · calculado · reconstruido ·
   supuesto · escenario · pendiente. En un registro, además: observación,
   opinión de un participante e interpretación propia van por separado.
5. **Una sensibilidad no es una probabilidad ni una recomendación.** Un
   escenario acota, un barrido muestra el corte y una simulación con
   distribuciones supuestas da frecuencias condicionales.
6. **Una definición, un dueño; el flujo, en un solo sentido:** fuente →
   proceso → resultado → presentación. Los originales no se tocan; un resultado
   malo se corrige en el proceso. Ante un dato roto, **fallar fuerte** en lugar
   de repararlo en silencio.
7. **Nada se valida con los datos con que se armó.** Un modelo se juzga fuera
   de muestra (y con el tiempo, partiendo por fecha), contra un benchmark
   ingenuo, y contando **todos** los intentos: si se probaron veinte
   configuraciones, alguna «funciona» por azar.

## Plantear antes de calcular

- **Separar la pregunta práctica de la pregunta de análisis.** «¿Me conviene
  X?» es la decisión; «¿bajo qué condiciones X conviene a este tipo de caso?»
  es la pregunta que el análisis puede contestar.
- **Clasificar antes de resolver:** qué es variable de elección, qué es
  parámetro, qué es restricción y qué es exógeno. La explicación válida es un
  cambio en algo observable que el agente no controla; «cambió algo no medido»
  (gustos, shocks ad hoc) explica todo y por eso no explica nada.
- **Unidad de análisis y comparación.** Sin grupo de comparación no hay
  inferencia; la escala de agregación cambia el resultado y lo agregado no
  habla de los individuos (falacia ecológica).
- **Alcance declarado:** qué tipo de trabajo es (descriptivo, explicativo,
  evaluativo) y qué no pretende. Describir no es explicar: si el pedido es
  describir, no se inventan causas.
- **Coherencia interna:** problema, objetivos, hipótesis, diseño y análisis se
  corresponden; un cambio en uno se revisa en los demás.
- **Subir el piso del pedido (profundidad).** Antes de resolver, contestá
  cuatro preguntas: ¿qué haría acá el mejor del oficio?, ¿cuál es el material
  más crudo disponible (la base, el registro, el plano, no el resumen)?, ¿con
  qué instrumento trabajaría (una base de datos, un modelo estadístico, un SIG,
  una simulación) en lugar de una tabla en texto?, y ¿qué, fuera de nosotros
  dos, confirmaría que está bien (una prueba que se pueda correr, un dato no
  visto, un tercero)? Si la respuesta cambia el pedido, proponé la versión
  mejorada al usuario antes de ejecutarla.

## Antes de usar una fuente externa

Respondé **qué mide, qué incluye y de cuándo es** (con o sin impuestos, flete o
montaje; región; escala; lista o negociado; nuevo o usado; nominal o real; ex
ante o ex post; qué precio exactamente). La fecha de descarga no es el período
que representa. Descargar no es poder redistribuir. Una etiqueta de la fuente
no es tu categoría analítica. Cada valor entra con fuente, fecha y rango. Ver
`referencias/fuentes-y-datos.md`. Para sacar los datos (consulta, descarga,
foto con su ficha y perfil al llegar), `quarry`.

## Los seis fundamentos, antes de cada cambio

| Fundamento | Qué pide |
|---|---|
| **Consistencia** | Las mismas convenciones en todo el trabajo (unidades, base de precios, período, definiciones); una sola versión de cada cosa. |
| **Eficiencia** | Reusar lo calculado; no hacer la misma cuenta en dos lugares. Complejidad sólo cuando el problema la tiene. |
| **Imaginación** | Si falta un dato, invertir la pregunta: calcular el valor al que la conclusión cambia (umbral, tasa de corte, precio de indiferencia). |
| **Flexibilidad** | Barridos y alternativas en lugar de un número; niveles que se reemplazan pieza por pieza al llegar el dato firme. |
| **Creatividad** | Al servicio de la evidencia: revela relaciones y decisiones; nunca maquilla la incertidumbre ni inventa un dato. Las ideas sin respaldo van en una «posdata» rotulada y no se filtran hacia atrás como evidencia. |
| **Innovación** | Herramientas que hacen auditable el trabajo: reproducción sin volver a la fuente, cálculo que se compara con otra implementación, pruebas, registro de cambios. |

## Validar contra la propia ilusión

- **Verdad conocida primero.** Antes de confiar en un método, que recupere lo
  que sembraste: datos simulados con parámetros conocidos (Monte Carlo), un caso
  de libro, una segunda implementación a mano. Y la contraprueba: sin señal
  sembrada, no debe declarar ganador.
- **Un resultado malo es información.** Se reporta tal cual (un acierto peor que
  una moneda, un VAN negativo). Si nada le gana al benchmark, se dice.
- **Los controles tienen límite declarado.** Que los totales cierren no prueba
  exactitud; decí qué no verifica cada control.
- **Identidades que cierran** (total = partes; lo ambiguo, aparte): el control
  ejecutable es de `hallmark`, nivel 2.
- **Condiciones antes que cálculos.** Verificar que la solución existe y es la
  que se cree (condiciones de segundo orden, estabilidad, que la restricción
  esté activa) antes de interpretarla. Resolver dos veces por caminos
  distintos. Probar los casos límite. Un resultado puede ser matemáticamente
  correcto y económicamente inválido.
- **Reproducir el dato publicado** antes de usarlo, con una columna de control
  que muestre la diferencia (y que sea sólo redondeo).
- **Diagnósticos que discrepan se reportan los dos**; no se elige el cómodo.

Detalle en `referencias/modelos-y-validacion.md`. Los controles del entregable
(cifras contra salidas, identidades, lectura final, revisión independiente, acta)
son de `hallmark`.

## Hábitos para pensar más allá del pedido

- **No casarse con un supuesto:** alternativas reales como opciones discretas, no como ±10 %.
- **Revisar el sistema de supuestos** (redundancia, suficiencia, independencia, consistencia) y buscar **la variable
  que decide**.
- **Contrafáctico:** ¿contra qué se compara? Escenarios acumulados de a un cambio.
- **Predicción refutable:** fechada, cuantitativa y distinta de la del marco alternativo.
- **Sustantivos a verbos** para encontrar el oficio que ya lo resolvió; se toma lo que hace, no se actúa el personaje.
- **Altitud:** la versión de más nivel se señala en la posdata rotulada, con su costo; no se ejecuta sin pedido.
- **Herramienta importada, supuestos importados.** Un modelo es un artefacto, no una descripción.
- **Un resultado demasiado bueno se interroga.** Estructura no es resultado, y el objeto reacciona.
- **Reportar los límites y no sobreafirmar.**

Detalle y ejemplos en `referencias/habitos.md`.

Para evaluación económica y financiera (tasas, costos de oportunidad, valor
terminal, riesgo de cola, políticas), ver `referencias/evaluacion-y-decisiones.md`.

## Registro y aprendizaje

Toda decisión material se anota con **Antes / Ahora / Por qué** y quién la
tomó. Los errores se clasifican (dirección, magnitud, medida contaminada,
supuesto caído, quiebre reflexivo) y sólo se destila una regla si es sobre el
método, no sobre el caso. Las lecciones se consultan antes de fijar una
magnitud. El prompt no aprende; el registro sí. En un proyecto de más de una
sesión, el registro vive en un archivo de estado; cuándo se lee y se escribe lo
dice `foreman`. La plantilla de ese archivo y la de una entrega
(conclusión con su nivel, opciones, lo que no se sabe) están en
`referencias/registro-y-comunicacion.md`.

## Cómo se combina

Esta skill es la forma de pensar: manda sobre el contenido de las demás. Las fases de un
trabajo y su dueño están en el ciclo de `foreman`; esta skill plantea al
principio, da los axiomas al analizar y registra al final.
Para repartir entre agentes, `tokenwise`. Si el proyecto tiene reglas propias
(un archivo de reglas, un documento de estado), mandan sobre esta skill cuando difieren.
