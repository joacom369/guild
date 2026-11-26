# Verificación y entrega

## Una ronda, acotada

```bash
python scripts/foto_pagina.py http://127.0.0.1:8000/ capturas/inicio --estricto
python scripts/foto_pagina.py http://127.0.0.1:8000/ capturas/inicio --oscuro --selector "#tablero"
python scripts/foto_pagina.py http://127.0.0.1:8000/ capturas/inicio --interacciones plan.json --json capturas/reporte.json --estricto
```

Saca escritorio (`1440×900`) y celular (`390×844`) en la misma corrida y corre una sonda automática AAA (se puede
desactivar con `--sin-sonda`):
- errores de consola, excepciones JS y recursos HTTP `>= 400` o fallidos (ignora `/favicon.ico`);
- desborde horizontal (`scrollWidth - clientWidth > 0`);
- imágenes rotas (`naturalWidth === 0`) y enlaces muertos (`href=""`, `href="#"`, `javascript:`);
- controles interactivos tapados en viewport (`elementFromPoint`), targets móviles `< 44×44 px` y controles sin
  nombre accesible en `Accessibility.getFullAXTree`;
- elementos visibles atascados en `opacity: 0` tanto en render normal como bajo `prefers-reduced-motion: reduce`.

Con `--interacciones plan.json` (inspirado en `storytold/photocraft`) ejecuta pasos (`click`, `fill`, `focus`, `key`
con `Escape`/`Tab`/`Enter`/flechas, `wait`) y valida relaciones (`visible`, `hidden`, `changed`, `text_contains`, `attr`,
`focused`, `count_min`). Con `--estricto`, cualquier defecto o fallo de interacción devuelve código `1`.

Leé las dos capturas y el informe, anotá todo lo que falla, corregilo en un lote y confirmá con una
ronda más como máximo.

Qué mirar en las capturas:
- ¿Se cumple el contrato? (modo, paleta, estructura, figura dominante).
- ¿Apareció algún anti-default?
- Jerarquía: ¿hay una sola cosa que manda en cada viewport?
- Celular: textos que se cortan, botones de menos de 44 px, tablas que empujan la página.
- Etiquetas superpuestas en gráficos, mapas o escenas.
- Estados de carga, vacío y error, al menos una vez.
- Si hay modo oscuro: los dos.

## Auditoría visual multi-estado

Validar sólo la captura inicial en reposo oculta fallos que aparecen recién al operar el entregable (etiquetas que se pisan al enfocar un período, barras de déficit invertidas, fugas de símbolos en modo ocultar montos o controles recortados dentro de pestañas secundarias).

Cuando la pantalla tiene controles interactivos, pestañas o escenarios, capturar y **mirar las imágenes** de todos los estados de estrés antes de entregar:

1. **Estado inicial** en escritorio (`1440×900`) y celular (`390×844`), en claro y oscuro si aplica.
2. **Pestañas o lentes secundarias** y una selección activa (p. ej. un período, modelo o filtro distinto del inicial).
3. **Escenario extremo o negativo / déficit** (comprobando línea cero real, escalas sin recorte y copys coherentes en zona negativa).
4. **Modo privacidad / ocultar montos** si existe (verificando cero fugas de `$` u otros valores monetarios fuera de la clase protegida, incluidos `<text>` de SVG).
5. **Diálogos abiertos (`<dialog>`)** sin cortes ni trampa de foco.
6. **Lupa geométrica en SVG/Canvas y estados hover/popover:** comprobar `getBBox()` (`0` textos recortados respecto al `viewBox` y `0` solapamientos), contornos de hover ajustados al píxel sobre el dato real y tooltips/popovers abiertos sin tapar el punto enfocado.

## Lo que las pruebas no ven

Las pruebas pueden pasar y la página verse rota (un capítulo que no carga, un script en el orden equivocado, un
color que no contrasta). Por eso la captura no se saltea, y por eso una prueba nueva que proteja lo que se rompió
vale más que tres que confirman lo que ya andaba.

## Entregar según el destino

| Destino | Antes de mandar |
|---|---|
| Página publicada (artifact u hosting) | Título de 2–4 palabras, tokens de color con modo oscuro, scripts sólo de CDNs permitidos con versión fija, nada confidencial en el HTML |
| Archivo autónomo (se abre sin conexión) | Todo embebido (CSS, JS, fuentes, modelos); abrirlo desde el disco y no desde el servidor; vigilar el peso |
| Carpeta para otra persona | Un LEEME con cómo abrirlo; nombres reservados reemplazados por su código; revisar el contenido final buscándolos |

**Sólo si sale a dominio público (no aplica a informes autónomos, tableros internos ni herramientas personales):**
- *Sitio público:* `meta description`, vista previa social (`og:image`), favicon real, `sitemap.xml` y `robots.txt`, página `404` propia e imágenes comprimidas (`WebP`/`AVIF`, con `width`/`height` explícitos para evitar saltos de layout).
- *Si además tiene backend, base o usuarios:* HTTPS activo, headers de seguridad (`CSP`, `HSTS`, `X-Content-Type-Options`), *rate limiting* y protección anti-spam en formularios públicos, backups verificados, monitoreo de errores y prueba real de *signup / login / reset*. Si hay claves filtradas en el historial de Git, se **rotan** (borrar el archivo no alcanza).
- *Legal y rastreo:* sin cookies no esenciales ni tracking **no** agregar banner de cookies; analítica sólo si el brief la pide; privacidad y términos generados como borrador requieren validación legal humana antes de publicar.

Si la página muestra cifras, antes de entregar corré `hallmark` (cada cifra buscada en las salidas, identidades,
acta). Cerrá con una o dos líneas: qué no se miró (otro navegador, un celular real, lectores de pantalla) y qué riesgo
queda.
