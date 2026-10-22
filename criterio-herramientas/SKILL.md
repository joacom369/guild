---
name: criterio-herramientas
description: Criterio para elegir la técnica o herramienta de ciencia de datos, estadística, econometría, análisis espacial o visualización (BI, tableros, Claude Dashboards, notebooks, modelos de ML) que conviene para una pregunta concreta, y para decir cuándo NO conviene. Recorre tipo de pregunta → candidatas con su supuesto clave → filtros de descarte (dónde nace la cifra, reproducibilidad, datos suficientes, lector, costo, confidencialidad) → veredicto «aplica / no aplica / todavía no» con su motivo. Usar cuando el usuario propone o pregunta por una técnica o herramienta («¿sirve X?», «¿y si usamos un modelo de…?», «¿esto sería como un Power BI?»), antes de construir un indicador o modelo, o al planear una visualización. También con /criterio-herramientas.
---

# Criterio de herramientas: la técnica sirve a la pregunta, no al revés

Complementa a `provenance` (cómo pensar cada cifra): esta skill decide **con qué** se contesta una pregunta y
**cuándo una herramienta no aplica**. Las decisiones son del usuario: tu tarea es darle un veredicto razonado, las
alternativas y lo que no se sabe. Si el proyecto tiene reglas propias (CLAUDE.md), mandan sobre esta skill.

## El procedimiento (cuatro pasos, siempre en este orden)

1. **Qué tipo de pregunta es.** Antes de nombrar una herramienta, clasificá la pregunta (tabla de abajo). Una pregunta
   mal clasificada elige mal la técnica: «¿dónde vendemos más?» es descriptiva; «¿por qué?» es causal y pide otra cosa.
2. **Candidatas, cada una con su supuesto clave.** Dos o tres, incluida siempre la más simple (un conteo, una tabla, una
   regla ingenua). Para cada una: qué supuesto exige y qué pasa si no se cumple. Catálogo en
   `referencias/catalogo.md`.
3. **Filtros de descarte.** Una candidata cae si falla cualquiera:

   | Filtro | Pregunta | Cae si… |
   |---|---|---|
   | **Origen de la cifra** | ¿Dónde se calcula el número? | Lo calcula la interfaz (un tablero que arma su propia consulta sobre crudos, una fórmula en una celda) en vez del proceso con pruebas. |
   | **Reproducible** | ¿Otro puede rehacerlo y obtener lo mismo? | No hay código, versión de datos o semilla; o depende de clics. |
   | **Datos suficientes** | ¿Hay n, eventos y variación para lo que pide? | n efectivo chico para el método (ver reglas de pulgar), sin grupo de comparación, sin variación en la variable que importa, o sin poder validar fuera de muestra. |
   | **Supuesto clave** | ¿Se cumple o se puede testear? | Se viola y no hay corrección (independencia con datos agrupados, estacionariedad, censura informativa, proporcionalidad). |
   | **Lector y uso** | ¿Quién lo lee y qué decide con eso? | El lector no puede interpretarlo, o la decisión no cambia con el resultado. |
   | **Costo y mantenimiento** | ¿Cuánto cuesta construirlo y sostenerlo? | Más caro que el valor de la decisión, o nadie lo mantiene después. |
   | **Confidencialidad** | ¿Dónde quedan los datos y quién los ve? | Saca precios, nombres o datos sensibles a un lugar no autorizado. |

4. **Veredicto**, uno de tres, con el motivo en una línea:
   - **Aplica:** pasa los filtros; decir con qué se valida (benchmark ingenuo, verdad conocida, fuera de muestra).
   - **No aplica:** qué filtro falla y qué conviene en su lugar.
   - **Todavía no:** qué falta (dato, definición, n, permiso) y qué haría falta para que aplique.

## Formato de la respuesta

```
Pregunta: … (tipo: …)
Candidatas:
  1. <técnica/herramienta> — supuesto clave: … — veredicto: aplica/no/todavía no — por qué: …
  2. …
Recomendación: … · Validación: … · Lo que no se sabe: …
```

## Tipos de pregunta

| Tipo | Ejemplo | Familia de técnicas |
|---|---|---|
| Descriptiva / monitoreo | ¿Cuánto facturamos por provincia? | Tablas, distribuciones, tableros que leen tablas publicadas |
| Comparación entre grupos | ¿Cierra más BA que Córdoba? | Tasas con intervalo, estratificación, modelos jerárquicos (shrinkage) |
| Tiempo hasta un evento | ¿Cuánto dura un servicio? | Supervivencia (Kaplan-Meier, Cox) con censura |
| Predicción / clasificación | ¿Será factible este sitio? | Regla ingenua → logístico → árboles; validación por fecha |
| Calibración | ¿La probabilidad del sistema acierta? | Curva de calibración, Brier, por tramos y por tipo |
| Espacial | ¿Dónde hay cobertura? | Distancia, densidad, interpolación; autocorrelación espacial |
| Serie temporal / pronóstico | ¿Cuánto vamos a facturar? | Ingenuo estacional, suavizado, ARIMA; quiebres |
| Causal / impacto | ¿La competencia baja el precio? | Diseños con comparación (dif-en-dif, discontinuidad, emparejamiento); si no hay, no se concluye causa |
| Segmentación | ¿Qué tipos de cliente hay? | Reglas de negocio primero; clustering sólo con validación de estabilidad |
| Concentración / estructura | ¿Dependemos de pocos? | Participaciones, Herfindahl, curva de Lorenz |
| Decisión con incertidumbre | ¿Conviene invertir? | VAN con barrido de tasa, umbral de indiferencia, escenarios; maximin si no hay probabilidades |
| Optimización / asignación | ¿A qué vendor pedirle? | Reglas, ranking con criterios explícitos; programación lineal sólo con objetivo y restricciones claros |

## Protocolo de modelado (cuando el veredicto es «aplica» y hay que estimar un modelo)

Se entrega en este orden, y el pre-análisis se muestra ANTES de los resultados:

1. **Pre-análisis:** unidad de análisis, distribuciones, outliers (qué son, si son errores o casos reales, qué se hace
   con ellos y por qué), composición de los grupos, datos faltantes y fuentes de sesgo posibles.
2. **Partición:** entrenamiento y prueba; con tiempo, por fecha (nunca al azar). El benchmark ingenuo se fija con el
   entrenamiento.
3. **Entrenamiento** sólo con el conjunto de entrenamiento; contar todas las especificaciones probadas.
4. **Diagnóstico:** sobreajuste (métrica en entrenamiento contra prueba), supuestos del método y su prueba, estabilidad
   (otra semilla, otro período), calibración si da probabilidades.
5. **Resultados y uso:** qué dice, con qué incertidumbre, para qué sirve y para qué no.

## Reglas de pulgar (señales, no leyes)

- **Logístico:** al menos 10–20 eventos por variable explicativa; con menos, menos variables o regularización.
- **Tasas por grupo:** con menos de ~10 eventos por celda, mostrar conteos e intervalos, no rankings; si hay muchos
  grupos chicos, contracción hacia la media (empírico-bayesiano o multinivel).
- **Kaplan-Meier:** la curva más allá de donde quedan pocos en riesgo no se lee; informar cuántos quedan.
- **ML complejo** (boosting, redes) sólo si un modelo simple validado ya le gana a la regla ingenua y sobra n.
- **Mapa coroplético** con grupos de tamaño muy distinto: muestra tamaño, no tasa; acompañar con n o usar puntos.
- **Un tablero** no es un análisis: sirve cuando la definición está cerrada y la pregunta se repite.

## Anti-patrones (si aparecen, frenar)

- **Herramienta buscando problema:** «usemos X» antes de tener la pregunta.
- **La interfaz calcula:** el tablero o el Excel define la métrica; dos tableros darán dos números.
- **Comparar grupos que difieren en composición** (la provincia que en realidad es un cliente; mezclar tipos de
  cotización): estratificar o comparar dentro del grupo.
- **Promedio sin distribución**, ranking sin intervalos, «significativo» sin contar los intentos.
- **Predecir sin benchmark ingenuo** o validar con los mismos datos.
- **Causalidad desde un corte transversal** sin diseño de comparación.
- **Sofisticación como señal de rigor:** lo simple bien especificado suele ganar.

## Cómo se combina

- Antes: `provenance` (axiomas, validación). Después del veredicto, la construcción sigue sus reglas.
- Para repartir trabajo con agentes: `tokenwise`.
- Si el proyecto tiene casos resueltos propios, se usan como ejemplo y prueba de la skill. Los de Providers LATAM
  están en el proyecto (`docs/CASOS_CRITERIO_HERRAMIENTAS.md`), no acá, porque tienen datos de la empresa.
