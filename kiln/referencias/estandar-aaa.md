# Estándar AAA de código, widgets y verificación (`kiln`)

Esta referencia fija el piso técnico HTML/CSS/JS y de interacción real de `kiln`. No repite las reglas visuales de
`impeccable` ([`craft-floor.md`](../../impeccable/reference/craft-floor.md), `polish`, `audit`) ni la exploración de
direcciones de `design-taste-frontend`: acá viven el **código**, los **widgets reales** y los **controles deterministas**.

## 1. Identidad propia (regla *clean-room*)

- Cada proyecto parte de su brief, su verbo y su `DESIGN.md`. Las referencias de
  [recursos-visuales.md](recursos-visuales.md) sirven para estudiar física, jerarquía o mecánica de un control,
  **nunca** para clonar paleta, tipografía, copy ni layout completo.
- Propiedad intelectual y licencias: de sitios comerciales o sin licencia abierta (como `bencho.dev` Pro) sólo se estudia
  el comportamiento visual o táctil (*clean-room*) y se construye una implementación propia en HTML/CSS/JS o con
  primitivas MIT explícitamente compatibles con el stack del proyecto.
- **Prueba de unicidad antes de codear:** revisar el contrato del paso 3 contra el brief; si alguna elección (paleta,
  tipografía, grilla o layout) serviría igual para un proyecto distinto, ajustarla y anotar qué se cambió antes de
  escribir código.

## 2. Piso técnico HTML y CSS

- **HTML semántico:** usar `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`; usar `<button type="button">` para
  acciones y `<a href="...">` real para navegación. Nunca usar `<div onclick>` ni `href="#"` sin destino real. En
  archivos HTML sueltos o servidores estáticos locales, declarar `<link rel="icon" href="data:,">` para evitar 404 ruidosos.
- **APIs nativas antes que librerías:** preferir `<dialog>` (cierre con `Escape` y `::backdrop` nativos), `popover`,
  `<details>`/`<summary>`, `@container` para tarjetas adaptativas, `:has()`, `clamp()` fluido, `font-variant-numeric: tabular-nums`
  para cifras, y `color-mix()` sobre tokens definidos en `:root`.
- **Movimiento sin degradar el render:** animar sólo propiedades compuestas (`transform`, `opacity`, `clip-path`, `filter`)
  con curvas `ease-out` exponenciales (`cubic-bezier(0.22, 1, 0.36, 1)`) y respuesta táctil al presionar (`scale(0.97)`
  en `:active`).
- **Movimiento reducido seguro:** toda animación de entrada bajo `@media (prefers-reduced-motion: reduce)` tiene que
  anular traslaciones y tiempos manteniendo **`opacity: 1` y visibilidad completa**; ninguna sección puede quedar atrapada
  en `opacity: 0`.

## 3. Widgets y gadgets interactivos reales

Tomado del enfoque de `storytold/photocraft` (*scorecard UI* y regla 15): **no se entrega ningún control decorativo,
falso o a medio conectar**. Si aparece en pantalla, responde de punta a punta o se quita antes de entregar.

Según lo que necesite el usuario, sumar gadgets reales y propios de la identidad del proyecto:
- **Navegación y búsqueda:** paleta de comandos (`⌘K`/`Ctrl+K`), filtro reactivo con conteo vivo y botón visible de
  «Limpiar filtros», ordenamiento reversible.
- **Controles táctiles:** conmutadores segmentados (`role="tablist"` + `aria-selected`) con indicador deslizable,
  comparadores o sliders con valor numérico visible en `tabular-nums`, inspectores laterales (*drawers*) en `<dialog>`.
- **Feedback honesto:** mensajes transitorios no intrusivos (*toasts* / barra de estado con `aria-live="polite"`) que
  nombran qué cambió o cómo reintentar si algo falla.
- **Coherencia de verbo (botón → feedback):** el control nombra exactamente la acción («Publicar», «Guardar cambios»,
  no «Enviar») y la confirmación repite el mismo verbo («Publicado»); los errores dicen qué pasó y cómo resolverlo, sin
  disculpas vagas.

Cada widget tiene que resolver:
1. Todos sus estados: `default`, `hover`, `focus-visible`, `active`, `disabled`, `loading`, `empty` y `error`.
2. Teclado completo (`Tab`, `Enter`/`Space`, flechas cuando hay grupo de pestañas/opciones) y cierre limpio con `Escape`
   sin trampa de foco.

## 4. Presupuestos e invariantes verificables

En la pasada única de [`../scripts/foto_pagina.py`](../scripts/foto_pagina.py) (escritorio `1440×900` y celular `390×844`):
- **Red e imágenes:** cero errores de consola y HTTP `>= 400`, cero `<img>` visibles con `naturalWidth === 0`.
- **Controles:** cero `<a>` muertos (`href="#"` o vacío), cero botones tapados (`elementFromPoint`), targets móviles
  `>= 44×44 px` y cero controles interactivos sin nombre accesible en el árbol `AXTree`.
- **Visibilidad y movimiento:** cero desborde horizontal (`scrollWidth <= clientWidth`) y cero secciones visibles
  atascadas en `opacity: 0`, tanto normal como con `prefers-reduced-motion: reduce`.
- **Pruebas de estado para widgets:** cuando la página tiene gadgets interactivos, acompañarla con un plan JSON para
  `--interacciones` que verifique relaciones (`visible`, `hidden`, `changed`, `focused`, `text_contains`, `attr`),
  evitando esperas por tiempos fijos. Lo que no se corrió se informa explícitamente como no medido.
- **Catálogo aislado en apps grandes:** usar `Storybook` (MIT) sólo en productos o apps grandes con librería propia de
  componentes donde conviene aislar y probar todos los estados (`loading`, `empty`, `error`, `disabled`); nunca en
  páginas sueltas o entregas chicas (`ponytail`).
