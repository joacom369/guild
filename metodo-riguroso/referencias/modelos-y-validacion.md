# Modelos y validación: el detalle

## Fuera de muestra
- El error de entrenamiento sobreestima el acierto: se reporta el de prueba.
- Con tiempo, se parte por fecha, nunca al azar. Purgar y dejar un embargo entre entrenamiento y prueba si las etiquetas se solapan.
- Cero mirada al futuro: plantar un shock en una fecha y comprobar que ningún dato anterior lo ve.
- Una sola partición es inestable: validación cruzada, y comparar con otra semilla. Fijar la semilla para reproducir y cambiarla para medir cuánto depende el resultado de ella.
- Hiperparámetros por validación, no a ojo. Cuando los criterios discrepan, dejar constancia.
- Expresar el error en unidades interpretables («se equivoca en promedio X en la unidad de la variable»).

## Contra qué se gana
- Siempre contra un benchmark ingenuo (1/N, el último valor, la media). Si ninguno le gana con una prueba significativa, el sistema no produce una recomendación y lo dice.
- Contar todos los intentos y ajustar por pruebas múltiples: el mismo desempeño pasa de aceptable a rechazado según cuántas configuraciones se probaron.
- Las pruebas respetan la estructura de los datos: con observaciones solapadas o dependientes, el n efectivo es mucho menor que el nominal.
- Un modelo ganador pero mediocre entra con su incertidumbre como confianza, no a pleno.

## Verdad conocida
- Monte Carlo con un proceso generador conocido: insesgadez, sesgo bajo supuestos débiles, eficiencia frente a otro estimador, tamaño y potencia.
- Reimplementar a mano y comparar con la función de la librería.
- Sembrar una señal y verla detectada; no sembrarla y no ver ganador.
- Bootstrap para la exactitud de un coeficiente cuando la teoría no alcanza.

## Supuestos del modelo
- Testearlos antes de usarlo, con la consecuencia escrita al lado («se rechaza normalidad: usar el módulo de colas»).
- Cada método documenta su dominio de validez.
- Aceptar sesgo para bajar varianza es un trade-off explícito; lo simple bien especificado le suele ganar a lo complejo.
- Fijar la expectativa antes de medir: en algunos problemas el techo realista es una ventaja marginal, no una predicción.
- Los patrones decaen: lo que se arbitra deja de funcionar.

## Interpretar
- Un coeficiente no significativo es ausencia de evidencia, no efecto cero.
- Cada coeficiente con su unidad, su categoría de referencia y su «manteniendo lo demás constante»; en log-log, como elasticidad.
- Multicolinealidad: preguntar por qué antes de regularizar.
- Graficar la distribución y los diagnósticos antes de modelar; prototipar la variable difícil en un caso antes de generalizar.

## Pruebas con personas (si el entregable las tiene)
Protocolo fijado antes de observar; orden alternado; no guiar; registrar las
intervenciones; medir «encontrar» y «lograr» por separado; no excluir sesiones
fallidas; con pocos participantes, exploratorio y sin porcentajes; metas de
tiempo después de medir una línea de base.

## Diagnóstico del modelo
- Si fallan los supuestos (heterocedasticidad, autocorrelación, normalidad,
  quiebre estructural), la hipótesis queda inconclusa y se dice qué haría falta.
- Series temporales: probar el orden de integración antes de regresar; niveles
  no estacionarios sin cointegración dan regresión espuria con t altísimos. Con
  cointegración, el largo plazo va en la relación de equilibrio y el corto en
  la corrección de error: diferenciar todo tira información.
- Quiebre estructural: anula la capacidad predictiva fuera del tramo.
- Una identidad (como MV = Py) no se testea; se testean los supuestos de
  comportamiento que la vuelven teoría.
- Antes de un modelo complejo, los diagnósticos que dicen si hace falta (por
  ejemplo, pruebas de dependencia en los residuos).
- La significatividad por permutación compara contra una línea base aleatoria:
  declarar cuántas permutaciones.

## Optimización y estática comparativa
- Verificar que existe solución (no singularidad, signos admisibles,
  restricción activa) antes de calcular.
- Condiciones de primer orden son necesarias; las de segundo orden, se chequean.
- Con desigualdades, comparar todas las soluciones candidatas (esquinas e
  interior) y encontrar el umbral del parámetro donde cambia la elección.
- El multiplicador (precio sombra) se interpreta con número y unidad: cuánto
  cambia el óptimo si la restricción se afloja en una unidad.
- Signo y magnitud de cada resultado con su lectura económica.
- Los supuestos estructurales se eligen para que el modelo dé signos
  refutables; si ningún resultado puede contradecirlo, no dice nada.
- La respuesta de corto plazo con factores fijos acota la de largo plazo; no
  tratar el ajuste parcial como total.
- Equilibrio no es eficiencia (un equilibrio puede ser ineficiente), y llegar
  al equilibrio no está garantizado: separar dónde está de si se llega
  (estabilidad), y nombrar el caso límite.
- Efecto total = directo + indirecto (como en una matriz de insumo-producto).

## Comparar métodos
- Fijar antes la partición, la semilla y la métrica, iguales para todos; al
  menos tres métodos; interpretar sólo el ganador.
- Riesgo (probabilidades estimables) no es incertidumbre (no lo son): la
  segunda pide criterios como maximin, no una simulación con probabilidades
  inventadas.
