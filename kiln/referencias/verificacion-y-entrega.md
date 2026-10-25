# Verificación y entrega

## Una ronda, acotada

```bash
python scripts/foto_pagina.py http://127.0.0.1:8000/ capturas/inicio
python scripts/foto_pagina.py http://127.0.0.1:8000/ capturas/inicio --oscuro --selector "#tablero"
```

Saca escritorio (1440×900) y celular (390×844) en la misma corrida, y reporta errores de consola y desborde
horizontal. Leé las dos capturas y el informe, anotá todo lo que falla, corregilo en un lote y confirmá con una
ronda más como máximo.

Qué mirar en las capturas:
- ¿Se cumple el contrato? (modo, paleta, estructura, figura dominante).
- ¿Apareció algún anti-default?
- Jerarquía: ¿hay una sola cosa que manda en cada viewport?
- Celular: textos que se cortan, botones de menos de 44 px, tablas que empujan la página.
- Etiquetas superpuestas en gráficos, mapas o escenas.
- Estados de carga, vacío y error, al menos una vez.
- Si hay modo oscuro: los dos.

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

Si la página muestra cifras, antes de entregar corré `hallmark` (cada cifra buscada en las salidas, identidades,
acta). Cerrá con una o dos líneas: qué no se miró (otro navegador, un celular real, lectores de pantalla) y qué riesgo
queda.
