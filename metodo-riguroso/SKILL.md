---
name: metodo-riguroso
description: Forma de pensar para trabajos con datos, modelos, evaluaciones, investigaciones o decisiones (tesis, informes, análisis económicos y financieros, proyectos de inversión, ciencia de datos, análisis espacial, tableros). Axiomas sobre el origen y el estado de cada cifra, seis fundamentos, validación contra la propia ilusión y hábitos para no casarse con un supuesto. Usar al empezar o revisar un trabajo analítico, antes de dar una conclusión, al cargar una fuente externa, al elegir o validar un modelo, o cuando el usuario pide rigor, metodología, sensibilidad o crítica. También con /metodo-riguroso.
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
4. **Cada cifra declara su naturaleza:** observado · calculado · reconstruido ·
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
`referencias/fuentes-y-datos.md`.

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
- **Identidades contables en cero:** total = asignados + sin coincidencia +
  ambiguos; un agregado calculado por vías distintas tiene que cerrar (el
  producto por producción, gasto e ingreso); lo ambiguo se informa aparte.
- **Condiciones antes que cálculos.** Verificar que la solución existe y es la
  que se cree (condiciones de segundo orden, estabilidad, que la restricción
  esté activa) antes de interpretarla. Resolver dos veces por caminos
  distintos. Probar los casos límite. Un resultado puede ser matemáticamente
  correcto y económicamente inválido.
- **Reproducir el dato publicado** antes de usarlo, con una columna de control
  que muestre la diferencia (y que sea sólo redondeo).
- **Diagnósticos que discrepan se reportan los dos**; no se elige el cómodo.

Detalle en `referencias/modelos-y-validacion.md`.

## Hábitos para pensar más allá del pedido

- **No casarse con un supuesto.** Alternativas reales (proveedores,
  tecnologías, financiamiento, comprar o alquilar) se modelan como opciones
  discretas con todas sus consecuencias, no como ±10 %. El caso base es lo más
  firme; lo demás va al lado, rotulado.
- **Revisar el sistema de supuestos:** no redundancia, suficiencia,
  independencia y consistencia. Ocho supuestos pueden ser tres puntos de falla.
  Identificá cuál restricción está activa en vez de asumirla.
- **Contrafáctico y escenarios acumulados.** ¿Contra qué se compara? Un base de
  «continuidad» y cambios agregados de a uno, para aislar el efecto de cada uno.
- **Buscar la variable que decide** (tornado) y poner ahí el esfuerzo de dato.
- **Predicción refutable y que discrimine:** fechada, cuantitativa, con su
  condición de refutación, y distinta de lo que predice el marco alternativo.
- **Sustantivos a verbos para encontrar disciplinas.** Reescribí el objeto
  como lo que hace: «el flujo de fondos» pasa a ser «convencer a un lector
  escéptico de una relación causa-efecto y decidir con incertidumbre». Cada
  verbo sugiere un oficio que ya lo resolvió (auditoría forense, periodismo de
  datos, edición). Se toma lo que ese oficio *hace*, no se actúa el personaje.
- **Mirar más allá del pedido, sin ejecutarlo (altitud).** Preguntá qué
  resultado hay detrás de la tarea («que no se caiga» detrás de «arreglá este
  error»). Si hay una versión de más nivel, se señala en la posdata rotulada,
  con su costo; no se ejecuta sin que el usuario la pida. El alcance lo fija
  el usuario.
- **Herramienta importada, supuestos importados:** declarar de qué disciplina
  viene, qué supuestos exige y si se cumplen. Rescatar la idea, no forzar la
  forma.
- **Un modelo es un artefacto, no una descripción:** sirve para lo que fue
  construido; coherencia interna no es validez externa, y la elegancia formal
  no reemplaza el contenido.
- **Un resultado demasiado bueno se interroga:** un VAN positivo sin una
  ventaja que lo explique (barreras, costo, información) suele ser un error de
  proyección o el sesgo de quien propone.
- **Estructura no es resultado, y el objeto reacciona:** el poder de un actor
  no implica el reparto; anunciar o analizar algo puede cambiarlo.
- **Crítica independiente** en las rondas grandes: alguien que no vio tu plan.
  Verificá sus hallazgos antes de aceptarlos.
- **Mirar el resultado real**, renderizado, y un caso individual concreto
  («la observación número 100») para ver que las variables tienen sentido.
- **Reportar los límites** y **no sobreafirmar**: antes de «siempre» o «a
  cualquier tasa», comprobar que vale en todas las alternativas.

Para evaluación económica y financiera (tasas, costos de oportunidad, valor
terminal, riesgo de cola, políticas), ver `referencias/evaluacion-y-decisiones.md`.

## Registro y aprendizaje

Toda decisión material se anota con **Antes / Ahora / Por qué** y quién la
tomó. Los errores se clasifican (dirección, magnitud, medida contaminada,
supuesto caído, quiebre reflexivo) y sólo se destila una regla si es sobre el
método, no sobre el caso. Las lecciones se consultan antes de fijar una
magnitud. El prompt no aprende; el registro sí. Ver
`referencias/registro-y-comunicacion.md`.

## Cómo se combina

Para ejecutar tareas de varias partes con el menor gasto, usá también
`reparto-eficiente`. Si el proyecto tiene reglas propias (un CLAUDE.md, un
documento de estado), mandan sobre esta skill cuando difieren.
