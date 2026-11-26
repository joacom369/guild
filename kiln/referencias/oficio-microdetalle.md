# Oficio de micro-detalle en tableros y widgets

Cómo llevar un entregable interactivo o de datos del nivel «prolijo y correcto» al nivel obsesivo al píxel: micro-instrumentos dentro de cada fila, popovers que cruzan vistas hermanas, paridad real entre modo claro y oscuro, y lupa geométrica antes de aprobar.

Complementa sin repetir el piso técnico de [estandar-aaa.md](estandar-aaa.md) y los objetos del dominio de [narrativa-creativa.md](narrativa-creativa.md). Toda referencia estudiada se aplica en modalidad *clean-room* (código e identidad propios).

## 1. Vocabulario de micro-instrumentos

En tableros e informes densos, evitar que todo sea tarjeta genérica o barra plana sin textura informativa:

- **Etiquetas directas al final de cada curva:** para 2 a 5 series temporales, apoyar el nombre y la cifra final (`tabular-nums`) pegados al extremo derecho del trazo en lugar de mandar al lector a una leyenda lejana; resaltar la serie activa y atenuar las pares al seleccionarla.
- **Micro-gráficos dentro de filas de tabla y tarjetas:** incorporar *tick-bars* (barras de rayitas verticales / tiras de confianza), barras segmentadas multicolores con desglose de estado y mini-sparklines o histogramas en línea para que cada fila cuente su trayectoria sin abrir otra pantalla.
- **Tramas con lectura estructural:** sumar áreas con trama de puntos o *hatch*, mapas coropléticos o de nube de puntos sobrios, arcos/gauges calibrados con marcas de escala, hipnogramas continuos por bandas y barras divergentes (impulsores positivos arriba de la línea `0`, negativos abajo) con curva de resultado neto superpuesta.
- **Tarjetas de duelo compacto (2 a 4 competidores):** mini-curva limpia sin ejes arriba + lista tabular debajo con punto de color por actor, porcentaje o magnitud tabular y píldora de variación (`pp`, `pb`, `%`) con fondo teñido semántico.

## 2. Popovers, tooltips e interacción sincronizada

- ***Cross-dimming* entre gráficos hermanos:** al pasar el foco por una categoría o barra en un panel, atenuar el resto en los paneles sincronizados (`opacity` ~`0,32–0,38`) y abrir un popover consolidado multimétrica; mostrar `—` honesto cuando una métrica no aplica, nunca `0`.
- **Tooltips estructurados con desglose:** usar tarjetas elevadas con encabezado (fecha o entidad), valor total arriba y filas de sub-estados con punto de color y `tabular-nums`; mover por `transform: translate(...)` (compuesto en GPU, sin reflow) y ubicar sin tapar el punto ni el dato enfocado.
- **Scrubbers temporales vivos:** acompañar series evolutivas con botón `Play`/`Pause` + slider continuo que reordena barras o rankings mes a mes; en carruseles o escenas automáticas, usar pastilla activa con barra de progreso lineal que se ensancha y se detiene al interactuar.
- **Tarjetas de anomalía o patrón accionables:** acompañar cada hallazgo cuantificado (patrón, desvío, incidente o umbral) con una acción directa al lado (`Inspeccionar`, `Filtrar`, `Revertir`, `Probar borde`), nunca una alerta pasiva sin salida.
- **Divulgación progresiva de alta densidad:** mantener limpia y respirable la vista principal; plegar por defecto exploradores multifiltro, tablas completas y buscadores de taxonomía larga con transición nativa (`interpolate-size: allow-keywords` + `@starting-style`), y estructurar mega-menús complejos con columnas escaneables y una pieza destacada única.

## 3. Paridad claro/oscuro, hilo cromático y atmósfera con propósito

- **Paridad real entre claro y oscuro:** diseñarlos como dos temas hermanos de igual cuidado (calibrando por separado líneas finas de `1 px` con `color-mix`, elevación por superficie, sombras y luminancia de acentos con contraste `>= 4,5:1` en subtítulos y ejes chicos; nunca inversión automática ni lavar rótulos a gris bajo).
- **Hilo cromático invariante:** cada entidad, país o categoría conserva exactamente el mismo color desde el resumen inicial hasta los gráficos `<canvas>`/`SVG`, tablas, popovers y miniaturas geométricas propias (sin fotos de stock).
- **Contraste tipográfico y textura con intención:** combinar con criterio (por ejemplo serif editorial de peso `600` + sans geométrica `tabular-nums`, o estética técnica de telemetría con micro-etiquetas en mayúsculas y monoespaciada sólo para coordenadas y cifras), fijar `size-adjust` en fuentes de respaldo para eliminar saltos, usar curvas de resorte sobrias (`ease-out` / `linear(...)`) y aplicar retículas de puntos o *dithering* contenido sólo donde refuerzan la lectura del dominio.

## 4. Lupa geométrica al píxel y guardarraíl (`ponytail` + `provenance`)

- **Cero recorte ni solapamiento en SVG (`getBBox()`):** en gráficos vectoriales con etiquetas vivas, ajustar altura dinámica del `viewBox` según cantidad de nodos, colapsar a 1 línea cuando la altura del nodo sea angosta (`< 28–30 px`), truncar con elipsis limpia cuando haga falta y verificar `0` textos recortados y `0` colisiones en modo real y en modo oculto.
- **Contornos y áreas hover fieles al dato:** el resaltado, trazo o caja interactiva se ciñe al píxel de la magnitud graficada, sin superponer bordes por encima de lo que se gastó o midió.
- **Unificación sin costuras:** evitar la convivencia de dos sistemas de tokens con radios o contrastes distintos en la misma página, y cuidar en `390 px` que la cabecera y el primer lienzo conserven el tono del bloque que encabezan.
- **Código mínimo con rigor de datos:** cada micro-instrumento responde una pregunta concreta desde filas publicadas (cero cifras decorativas ni rellenos inventados) y se implementa en SVG, Canvas o CSS nativos salvo necesidad real.
