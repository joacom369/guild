# Catálogo: técnica por tipo de pregunta, con su supuesto clave y cuándo no

Cada entrada: **candidatas** (de la más simple a la más compleja) · **supuesto clave** · **no aplica si** · **datos
mínimos** · **herramientas**. Las herramientas son ejemplos; la elección final pasa por los filtros del SKILL.md.

## Descriptiva y monitoreo
- **Candidatas:** tabla con conteos y totales; distribución (mediana, percentiles); serie mensual; tablero.
- **Supuesto clave:** la definición está cerrada (qué es «activo», «venta», «país»).
- **No aplica si:** la definición todavía se discute (primero se escribe y se prueba en el proceso), o el tablero
  calcularía la métrica por su cuenta.
- **Herramientas:** pandas → CSV publicado; Superset o un tablero (Claude Dashboards, Power BI) **leyendo tablas
  publicadas del modelo**, nunca crudos.

## Comparación entre grupos (provincias, vendedores, vendors)
- **Candidatas:** tasa con intervalo (Wilson) y conteo; estratificar por la variable de composición; modelo multinivel
  o empírico-bayesiano para muchos grupos chicos.
- **Supuesto clave:** los grupos son comparables en composición (mismo tipo de cliente, canal, producto), o se controla.
- **No aplica si:** cada grupo es casi un solo cliente o caso (la comparación mide al cliente, no al grupo); celdas con
  menos de ~10 eventos sin contracción.
- **Herramientas:** statsmodels (proporciones, GLM), PyMC/bambi o lme4 para multinivel.

## Tiempo hasta un evento (duración, respuesta, baja)
- **Candidatas:** Kaplan-Meier por grupo; log-rank; Cox si hay covariables; modelos paramétricos para extrapolar.
- **Supuesto clave:** censura no informativa; en Cox, riesgos proporcionales (testear con residuos de Schoenfeld).
- **No aplica si:** se descartan los casos abiertos (sesgo), el evento no está bien fechado, o se mide con cambios de
  estado que no son el evento.
- **Herramientas:** lifelines, survival (R).

## Predicción y clasificación
- **Candidatas:** regla ingenua (la que usa hoy el equipo) → logístico con pocas variables → árboles/boosting.
- **Supuesto clave:** el futuro se parece al pasado del entrenamiento; las variables están disponibles al momento de
  predecir (sin filtrar el resultado).
- **No aplica si:** no se puede partir por fecha; pocos eventos por variable; no hay benchmark contra el que ganar.
- **Herramientas:** scikit-learn (con `TimeSeriesSplit`), statsmodels para el logístico interpretable.

## Calibración de probabilidades
- **Candidatas:** tabla por tramos (predicho contra observado) con n por tramo; Brier y su descomposición; curva de
  confiabilidad.
- **Supuesto clave:** el resultado real está bien definido y no se reescribe la probabilidad después del resultado.
- **No aplica si:** se mezclan poblaciones con escalas distintas (calibrar dentro de cada tipo).
- **Herramientas:** scikit-learn (`calibration_curve`), pandas.

## Espacial
- **Candidatas:** distancia al antecedente más cercano; densidad por celda (H3); interpolación (kriging) sólo con
  variable continua; autocorrelación (Moran) para saber si hace falta modelo espacial.
- **Supuesto clave:** la ubicación está bien geocodificada; la unidad espacial no cambia la conclusión (MAUP).
- **No aplica si:** los puntos son centroides o nombres de ciudad; se interpreta un mapa coroplético de grupos con n
  muy distinto como tasa.
- **Herramientas:** shapely, geopandas, h3, PySAL; QGIS para revisar a ojo.

## Serie temporal y pronóstico
- **Candidatas:** ingenuo estacional; suavizado exponencial; ARIMA/ETS; regresión con quiebres.
- **Supuesto clave:** estacionariedad o modelo de la tendencia; sin quiebres no modelados.
- **No aplica si:** la fuente tiene huecos (meses con caída de facturación), pocos períodos, o regímenes distintos
  (cepo, cambio de moneda) sin tratar.
- **Herramientas:** statsmodels (ETS, SARIMAX), pmdarima.

## Causal / impacto
- **Candidatas:** comparación antes-después con grupo de control (diferencias en diferencias); discontinuidad;
  emparejamiento; experimento si se puede.
- **Supuesto clave:** el grupo de control representa el contrafáctico (tendencias paralelas, sin selección).
- **No aplica si:** sólo hay un corte transversal; la «causa» se eligió mirando el resultado. Entonces se describe y
  se dice que no se concluye causa.
- **Herramientas:** statsmodels/linearmodels, DoWhy.

## Segmentación
- **Candidatas:** reglas de negocio explícitas; k-means/jerárquico con variables estandarizadas; perfiles.
- **Supuesto clave:** los segmentos son estables (otra semilla u otro período dan lo mismo) y accionables.
- **No aplica si:** no hay decisión distinta por segmento; los segmentos cambian con la semilla.
- **Herramientas:** scikit-learn; validar estabilidad con remuestreo.

## Concentración y estructura
- **Candidatas:** participación del primero y de los cinco primeros; Herfindahl; curva de Lorenz.
- **Supuesto clave:** la unidad está bien definida (cliente = cluster, con apertura por cliente final).
- **No aplica si:** se mezclan niveles (holding con filial).

## Decisión con incertidumbre (inversión, renegociación)
- **Candidatas:** VAN/TIR con barrido de tasa; umbral de indiferencia; escenarios discretos; Monte Carlo sólo con
  distribuciones defendibles; maximin/minimax-regret si no hay probabilidades.
- **Supuesto clave:** los flujos y la tasa están en la misma moneda y base (nominal/real).
- **No aplica si:** se presenta una simulación con probabilidades inventadas como riesgo medido.

## Optimización y asignación
- **Candidatas:** ranking con criterios explícitos y pesos a la vista; programación lineal/entera.
- **Supuesto clave:** el objetivo y las restricciones son los reales y medibles.
- **No aplica si:** los pesos son arbitrarios y nadie los validó; el «óptimo» depende de un dato que no existe.
- **Herramientas:** pandas para rankings; PuLP/OR-Tools.

## Visualización y tableros
- **Candidatas:** página estática generada desde el pipeline; Superset; Claude Dashboards; Power BI; Excel con
  colores de rol (entrada, cálculo, resultado).
- **Supuesto clave:** la cifra ya existe en una tabla publicada y probada; el tablero sólo la dibuja.
- **No aplica si:** el tablero arma su propia consulta sobre los crudos; la herramienta no puede conectarse a la fuente
  real; los datos son confidenciales y salen de donde están autorizados.
