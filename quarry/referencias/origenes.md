# Orígenes: el detalle por tipo

Lo común a todos está en el SKILL.md. Acá, lo que cambia según de dónde sale el dato.

## Base de datos (SQL)

- Primero el esquema y un `COUNT(*)` con los mismos filtros; después la consulta.
- Columnas explícitas; filtros y agregaciones en la base, no en Python.
- Paginación por clave (`WHERE id > :ultimo ORDER BY id LIMIT n`) antes que `OFFSET`, que se vuelve lento y puede
  saltear filas si la tabla cambia durante la extracción.
- Las fechas, con zona horaria explícita; los montos, con su moneda y si incluyen impuestos.
- Un `JOIN` dentro de la consulta multiplica filas si no es 1:1: contá antes y después.
- Una vista o un modelo intermedio (de un warehouse, de dbt) ya trae definiciones: anotá cuál se usó, porque «ventas»
  en dos vistas puede no ser lo mismo.

## API (REST, GraphQL, servicios geográficos)

- Leé la documentación del límite de pedidos y del tamaño de página; respetá los dos.
- Guardá cada respuesta cruda (JSON) antes de transformarla: si la transformación falla, no hay que volver a pedir.
- Comparar el total anunciado (`total`, `count`, `numberMatched`) con lo recibido.
- Paginación por cursor cuando existe; si es por número de página, orden estable.
- Errores `429` o `5xx`: espera creciente y reintento acotado. Un `4xx` distinto no se reintenta: se corrige.
- Credenciales fuera del código y fuera de la ficha.

## Conector MCP o herramienta de un agente

- Mirá la descripción de cada herramienta: algunas mezclan lectura y escritura. Usá sólo las de lectura.
- Muchas devuelven un resumen o un recorte (primeras N filas, texto truncado). Si el resultado dice «truncado»,
  «incompleto» o trae un cursor, no está entero: seguí paginando o achicá la consulta.
- Si el resultado grande queda guardado en un archivo, procesalo desde ahí con un script; no lo leas entero en el
  contexto.
- Anotá en la ficha el nombre del conector y de la herramienta, con los parámetros usados.

## Planillas y archivos

- Lo que entra es una copia: anotá de dónde salió, quién la mandó y de qué fecha es la versión.
- En una planilla, la fila de encabezado puede no ser la primera, hay celdas combinadas, totales mezclados con datos y
  fórmulas cuyo valor guardado puede estar desactualizado. Leé los valores, no las fórmulas, y sacá los totales.
- Formatos regionales: `1.234,5` es mil doscientos treinta y cuatro con cinco en Argentina y mil y pico en EE. UU.
  Fijalo al leer; no lo adivines.
- Codificación (UTF-8, Latin-1) y separador (`,` o `;`) explícitos.

## Web (páginas, tablas publicadas, descargas)

- Preferí la descarga oficial (CSV, API) a raspar la página.
- Si se raspa: respetá `robots.txt` y los términos de uso, pausá entre pedidos y guardá el HTML crudo.
- Descargar no es poder redistribuir: anotá la licencia.
- Una cifra de una nota periodística no es la fuente: buscá el original.

## Extracciones repartidas entre agentes

Cada agente devuelve **archivos con su ficha**, no filas en el texto. El encargo dice qué origen, qué filtros, qué
carpeta y qué control corre antes de devolver (`perfil.py`, el total anunciado contra el recibido). Ver `tokenwise`.
