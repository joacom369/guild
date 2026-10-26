---
name: quarry
description: Procedimiento para sacar datos de cualquier origen (base SQL, API, conector MCP, planilla, archivo, página web) sin romper la fuente y con la procedencia guardada. Estima antes de consultar (cuántas consultas, cuánto pesan, cuánto tardan) y espera el visto bueno, prueba con una muestra, pagina y compara el total anunciado con el recibido, guarda una foto de los datos con su ficha (consulta, origen, fecha, período, hash) y termina con un perfil que separa nulos de ceros y revisa claves y cruces. Usar antes de una extracción o descarga, al traer datos de un sistema, al cruzar dos bases, o con /quarry. No decide qué técnica usar (`compass`) ni qué significa cada campo de un sistema (para eso, la skill de dominio de ese ambiente, que manda sobre esta).
argument-hint: "[qué datos y de dónde]"
---

# Quarry: sacar el bloque sin romper la veta

En una cantera se estudia el frente antes de cortar, se saca una muestra, se corta con método y cada bloque sale
marcado con el frente del que salió. Con los datos es igual: **el dato vale lo que vale su procedencia**. Esta skill
es el procedimiento; el criterio sobre cada cifra está en `provenance`.

Sirve para cualquier ambiente. Las reglas propias de cada uno (qué sistemas son de sólo lectura, qué no se puede
sacar, quién autoriza) están en las reglas del proyecto o del usuario y **mandan sobre esta skill**. Si el ambiente
tiene skills de dominio sobre sus datos (cómo se accede a cada sistema, qué fuente es la verdad para cada dato, qué
significa cada campo), **cargalas antes del paso 1**: esta skill pone el procedimiento y ellas, el conocimiento.

## Las reglas (no se negocian)

1. **Sólo lectura por defecto.** Una extracción no escribe, no borra, no manda mensajes ni dispara procesos en el
   origen. Si la herramienta mezcla lectura y escritura, se usan sólo las de lectura.
2. **Nada se transcribe a mano.** El resultado completo va a un archivo, y de ahí a un script. Copiar filas desde la
   pantalla, o encargarle a un agente que las copie, es caro y mete errores.
3. **Lo que se sacó y lo que existe son cosas distintas.** «Cero filas en la consulta» no es «no hay»: puede ser un
   filtro, un permiso, una página truncada o un sistema caído. Se reporta como lo que es.
4. **Una corrida nueva no pisa la anterior.** Cada foto lleva fecha en el nombre de la carpeta.
5. **Un intento fallido queda anotado como caso**, con el error tal como salió. No se ofrece como dato.

## El procedimiento

### 1. Reconocer el frente (antes de consultar)

- **Qué pregunta contesta este dato** y qué columnas hacen falta de verdad. Se pide lo necesario, no `SELECT *`.
- **Qué es el origen:** sistema, tabla o endpoint, quién lo mantiene, cada cuánto se actualiza y qué período cubre.
  La fecha de extracción no es el período que el dato representa.
- **Qué devuelve la herramienta:** si pagina, si tiene un tope de filas, si filtra del lado del servidor, si el
  resultado llega entero o resumido.
- Una consulta barata de reconocimiento si existe: `COUNT(*)`, el total que anuncia la API, el esquema, los metadatos.

### 2. Estimar y esperar el visto bueno

Antes de una extracción que no sea trivial, decile al usuario en una o dos líneas:

> Son **N consultas** (o páginas) de unas **F filas** cada una, **≈ P MB** en total, **≈ T minutos**. Se guardan en
> `<carpeta>`. ¿Sigo?

Si hay que estimar a ciegas, decí que es una estimación y de dónde sale. Esperá la respuesta cuando la extracción es
larga, pesada, cara o golpea un sistema compartido; para una consulta chica y acotada alcanza con avisar.

### 3. Muestra primero

Una página o `LIMIT 100`, y mirala: ¿están las columnas?, ¿las unidades son las que se creían?, ¿las fechas vienen en
el formato esperado?, ¿los códigos tienen sentido? Corregí la consulta acá, que es barato.

### 4. Cortar con método

- **Filtrar del lado del servidor**, no traer todo para filtrar después.
- **Paginar con orden estable** (una clave única en el `ORDER BY`); sin orden, las páginas se pisan o se saltean filas.
- **Comparar el total anunciado con el recibido**; detectar páginas repetidas o truncas.
- **Pausar entre pedidos** y poner un tope de tamaño; respetar los límites del servicio.
- **Reintentos acotados** (dos o tres, con espera creciente). Si sigue fallando, se para y se informa.
- Un resultado grande que la herramienta guarda en un archivo **se procesa desde ese archivo** con un script, con el
  conteo de filas contra la consulta de control.

Detalle por tipo de origen (SQL, API, conector MCP, planillas, web) en
[referencias/origenes.md](referencias/origenes.md).

### 5. Marcar el bloque (la foto y su ficha)

```bash
python scripts/ficha.py datos/2026-10-25_ventas/ --origen "warehouse.ventas" --consulta consulta.sql \
       --periodo "2026-01..2026-09" --nota "sin anuladas"
python scripts/ficha.py datos/2026-10-25_ventas/ --verificar
```

`ficha.py` escribe `FICHA.json` en la carpeta: origen, consulta (texto o archivo), fecha de extracción, período
representado, herramienta, filas y columnas de cada archivo y su hash SHA-256. `--verificar` recalcula los hashes
y falla si algo cambió: se corre antes de recalcular cualquier resultado.

- La **consulta** se versiona (en el repo); los **datos** no, salvo que el proyecto diga otra cosa.
- Los originales no se tocan. La limpieza produce otro archivo, en otra carpeta.

### 6. Perfil al llegar

```bash
python scripts/perfil.py datos/2026-10-25_ventas/ventas.csv --clave id_venta
python scripts/perfil.py ventas.csv --clave id_venta --cruzar clientes.csv --por id_cliente
```

Por columna informa: vacíos (nulos, celdas en blanco, `NA`) **separados de los ceros**, distintos, mínimo y máximo, y
valores de ejemplo. Con `--clave`, si la clave es única y cuántas filas repiten. Con `--cruzar`, la cardinalidad del
cruce: cuántas filas encuentran exactamente una pareja, cuántas ninguna y cuántas más de una. Esas tres cuentas
suman el total: lo ambiguo se informa aparte, nunca se descarta en silencio.

El perfil se lee y se comenta: un 40 % de vacíos en una columna clave o un cruce 1:N que se creía 1:1 cambia el
análisis y se le dice al usuario antes de seguir.

### 7. Entregar la extracción

Una línea con lo que hay: «Saqué F filas de `<origen>` (período P), foto en `<carpeta>` con su ficha. Total anunciado
= recibido. Vacíos relevantes: …; cruce con … : X sin pareja, Y ambiguos. No saqué: …». Lo que falló o quedó afuera
va a la vista.

## Scripts

Sólo biblioteca estándar de Python para CSV, TSV y JSON. Los dos scripts cargan cada tabla entera en memoria: van
bien hasta unos cientos de miles de filas; para más, perfilá una muestra o hacé el perfil en la base con SQL. Para `.xlsx` hace falta `openpyxl` y para `.parquet`,
`pandas` con `pyarrow`; si faltan, el script lo dice y no sigue. Ayuda con `python scripts/<script>.py -h`.

## Cómo se combina

- `provenance`: qué es cada cifra (su vocabulario de naturaleza es el único) y cómo se interroga una fuente externa.
- `tokenwise`: si la extracción se reparte entre agentes, cada uno devuelve archivos con su ficha, no filas copiadas.
- `hallmark`: antes de entregar, cada cifra del informe se busca en las salidas que salieron de esta foto.
- `compass`: si la pregunta es qué herramienta usar para analizar lo extraído.
