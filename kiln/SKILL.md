---
name: kiln
description: >
  Punto de partida para construir un entregable que tiene que salir pulido desde el primer intento y no con el
  aspecto genérico de plantilla: el frontend de una página web, un tablero, un recorrido o un informe en HTML (con
  tablas, gráficos, presentaciones o 3D), y también un documento, una planilla, una presentación o un PDF. Entiende qué busca el usuario, le ofrece direcciones con vista previa, fija un
  contrato de diseño, construye con código mínimo, se mira en escritorio y celular, y deriva el pulido a las
  skills compañeras. Usar al empezar una página o un rediseño, cuando el usuario pide "que quede lindo",
  "más diseño", "landing", "dashboard", "tablero", "recorrido", "página", "frontend", "UI/UX", "armá el informe en
  Word", "la presentación", "la planilla para el equipo", o con /kiln. La mecánica de cada formato de archivo la
  ponen las skills de archivos de la plataforma.
  No decide si hace falta un tablero (`compass`) ni controla las cifras que muestra (`hallmark`).
argument-hint: "[qué se construye]"
license: MIT
---

# Kiln

El horno donde el barro se vuelve pieza. Esta skill no repite lo que ya hacen las compañeras: decide **qué** se
construye con el usuario, fija el **cómo** antes de tocar código, y no entrega nada que no se haya mirado.

Es la dueña de la fase 5 para cualquier entregable. Lo que sigue está escrito para HTML; un documento, una planilla,
una presentación o un PDF siguen los mismos pasos con lo que cambia en
[referencias/archivos.md](referencias/archivos.md).

## 0. Compañeras

Mirá la lista de skills disponibles (no el disco) y usá las que estén:

| Skill | Cuándo |
|---|---|
| `design-taste-frontend` | Pasos 2 y 3: proponer direcciones y fijar la dirección visual de algo nuevo, sin defaults de plantilla. Viene marcada para no cargarse sola: leé su `SKILL.md` en la carpeta de skills (o pedile al usuario que la invoque por su nombre). |
| Recursos visuales | Si el brief pide textura o movimiento: [referencias/recursos-visuales.md](referencias/recursos-visuales.md). |
| `impeccable` | Paso 6: `polish` al terminar cada página, `audit` antes de entregar; `document` para el sistema. |
| `ponytail` | Paso 4: todo el código. Si no está, aplicá sus reglas igual (ver paso 4). |
| `developing-with-streamlit` | Si el proyecto es Streamlit. |
| Skills de archivos (`docx`, `xlsx`, `pptx`, `pdf`) | Si el entregable es un archivo: ponen la mecánica del formato. |
| `provenance` | Si la página muestra cifras de un modelo o un análisis. |
| `compass` | Antes del paso 2 en un tablero: ¿hace falta una página, o la cifra ya está publicada en otro lado? |
| `dataviz` | Al construir gráficos, paletas de series y fichas de cifras. |
| `quarry` | Si los datos de la página hay que sacarlos de un sistema. |
| `assay` | Si las cifras de la página salen de un análisis: se construye desde su carpeta de salidas. |
| `hallmark` | Antes de entregar una página con cifras: cada número buscado en las salidas y acta de controles. |

Si falta una que mejoraría el resultado, decilo **una vez**, en concreto, y seguí sin ella:
«El resultado mejora con `impeccable` (pulido y auditoría; github.com/pbakaus/impeccable). No está instalada:
¿la instalo?». De las demás, nombrá la skill y que se busque por su nombre; no inventes URLs. **Nunca instales una
skill, un paquete ni los hooks de `impeccable` sin la confirmación del usuario.**

## 1. Leer antes de preguntar

Averiguá solo lo que se puede averiguar: `DESIGN.md` o `PRODUCT.md` del proyecto, el stack y sus componentes, las
páginas que ya existen, la marca si la hay ([referencias/marca.md](referencias/marca.md)), las referencias que dejó el
usuario. No se pregunta lo que el repositorio contesta.

## 2. Entender qué busca (entrevista corta)

Antes de pensar en la forma, pasá el sustantivo a verbo: no «una presentación», sino «que el directorio entienda por
qué cayó el margen y decida». Lo que se construye sale del verbo.

- **Pedido claro:** enunciá tu lectura en una línea y avanzá. «Lo leo como: tablero de seguimiento para el
  equipo comercial, sobrio, oscuro, cifras protagonistas.»
- **Pedido vago:** ofrecé 2 a 4 **direcciones concretas** con `AskUserQuestion`, cada una con vista previa (boceto
  ASCII del layout o fragmento de la paleta y la tipografía), la recomendada primero con «(Recomendado)». El usuario
  siempre puede elegir «Otro» y describir lo suyo: eso es parte del diseño, no un desvío.
- Máximo 1 a 3 preguntas, y sólo las que cambian el resultado (propósito, público, tono, densidad). Sin la
  herramienta, las mismas opciones en texto, numeradas.
- Las direcciones salen del catálogo: [referencias/direcciones.md](referencias/direcciones.md).

## 3. Contrato de dirección

Antes del código, en pocas líneas que el usuario ve y puede corregir:

- **Modo:** convencer, operar, leer o vivir la experiencia (qué es éxito para quien la visita).
- **Paleta** por roles (fondo, tinta, acento, estado) y **tipografía** (títulos, cuerpo, cifras).
- **Estructura:** el esqueleto de la página y la figura dominante de cada sección.
- **Movimiento y densidad**, y **qué se evita** (de [referencias/anti-defaults.md](referencias/anti-defaults.md)).
- **Lo que afirma:** cada sección como una afirmación con su prueba (una cifra, una foto real, un caso). La
  sección sin afirmación se saca.
- **Referencias**, si las hay.

Si existe `DESIGN.md`, el contrato lo extiende; no lo contradice sin decirlo.

## 4. Construir: ambición en el diseño, pereza en el código

El diseño apunta alto; el código, al mínimo que lo resuelve entero (reglas de `ponytail`):

- Lo que el proyecto ya tiene (componentes, tokens, utilidades) antes que lo nuevo. CSS nativo antes que una
  librería. Ninguna dependencia por unas pocas líneas; si se agrega, con versión fija.
- Sin abstracciones, opciones ni código «para después». Comentarios sólo del porqué.
- Tokens en `:root` (color, espacio, tipo); los valores no se repiten sueltos.
- Datos reales o verosímiles, nunca «Lorem ipsum» ni «Item 1». Con cifras de un modelo:
  [referencias/datos-en-pantalla.md](referencias/datos-en-pantalla.md).
- Tablas, presentaciones y gráficos dentro del HTML:
  [referencias/tablas-y-presentaciones.md](referencias/tablas-y-presentaciones.md). 3D:
  [referencias/3d-web.md](referencias/3d-web.md).

**Piso que no se negocia** (no es «beta» si falta, es incompleto):
- se lee y se usa a 390 px de ancho, sin scroll horizontal;
- contraste de cuerpo ≥ 4,5:1, foco visible, navegable con teclado, `alt` en imágenes con contenido;
- donde algo carga: estado de carga, vacío y error;
- consola sin errores.

**Sólo si el brief o el proyecto lo piden:** modo oscuro, animación más allá de transiciones, 3D, interacción
compleja. Pereza no es recortar el piso; ambición no es sumar lo que nadie pidió.

## 5. Mirarse antes de mostrar (una ronda, acotada)

Con [scripts/foto_pagina.py](scripts/foto_pagina.py): escritorio y celular **juntos**, en una sola ronda. Revisá
las capturas contra el contrato y la lista de anti-defaults, más el informe de errores y desborde del script.
Corregí todo en un solo lote, confirmá con **una** ronda más como máximo, y pará. Las pruebas en verde no
alcanzan: una página puede pasar todas y verse rota. Detalle en
[referencias/verificacion-y-entrega.md](referencias/verificacion-y-entrega.md).

## 6. Pulir, entregar y dejar registro

- `impeccable polish` sobre lo terminado; `impeccable audit` antes de entregar.
- Entregá según el destino (página publicada, archivo autónomo, carpeta para otro):
  [referencias/verificacion-y-entrega.md](referencias/verificacion-y-entrega.md).
- Si se decidió algo del sistema (un token, un componente, una regla), va al `DESIGN.md` del proyecto
  (`impeccable document`), para que la próxima página arranque desde ahí.
- Cerrá con una o dos líneas: qué no se miró y qué riesgo queda.

## Quién manda cuando chocan

1. El pedido del usuario y el `DESIGN.md` del proyecto («el brief gana»: una paleta o una fuente pedida se
   respeta aunque esté en una lista de evitar).
2. La lista de anti-defaults de esta skill.
3. Los defaults de `design-taste-frontend` y de `impeccable`.
4. La ambición es del diseño; la pereza, del código (`ponytail`). El piso del paso 4 no lo baja ninguna.
