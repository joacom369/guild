# Tablas, planillas y presentaciones dentro de una página

Cuando el HTML trae una planilla, un cuadro grande o una presentación, tiene que verse igual de bien que el resto,
en escritorio y en celular.

## Tablas y planillas

- `<table>` semántica con `<caption>` (o un título visible) y `<th scope>`; nada de grillas de `<div>`.
- Contenedor con `overflow-x: auto` y la tabla adentro: la página nunca se desborda, la tabla sí puede.
- Encabezado fijo (`position: sticky; top: 0`) y, en tablas anchas, primera columna fija.
- Cifras alineadas a la derecha y con `tabular-nums`; texto a la izquierda. Unidad en el encabezado, no en cada
  celda.
- Subtotales y totales con peso tipográfico, no con color. Separadores finos, sin zebra si las filas son pocas.
- En celular: si la tabla tiene más de 4–5 columnas, ofrecé una vista apilada por fila o elegí las columnas que
  importan, con la tabla completa a un toque.
- Si es editable (planilla): celdas con foco visible, navegación con flechas y `Enter`, y la validación en la
  celda que falla.
- Exportar a CSV o Excel con el mismo contenido que se ve, no con otro cálculo.

## Presentaciones

- Escenario fijo 16:9 escalado para entrar en la ventana (`aspect-ratio: 16 / 9` y `transform: scale` o
  unidades de contenedor); el contenido nunca se reacomoda por el ancho.
- Navegación con flechas, barra espaciadora, `Inicio` y `Fin`; número de diapositiva visible; enlace directo a
  cada una (`#3`).
- Una idea por diapositiva: título que dice la conclusión, una figura o una cifra, poco texto.
- `@media print` con `@page { size: landscape; margin: 0 }` y un salto por diapositiva, para exportar a PDF
  limpio desde el navegador.
- Si lo que se pide es una presentación de verdad para compartir, el tipo de artifact de diapositivas (Slides)
  existe y exporta a .pptx y PDF: preferilo a armar una a mano.

## Gráficos

- SVG o una librería ya presente en el proyecto; una nueva sólo si el gráfico lo exige (con versión fija). En proyectos React donde SVG nativo no alcanza, `Recharts` (MIT) es la opción por defecto, siempre bajo [datos-en-pantalla.md](datos-en-pantalla.md).
- Mismos tokens de color que la página; texto del gráfico como texto, no dentro de una imagen.
- Tabla alternativa o `aria-label` con la lectura del gráfico.
