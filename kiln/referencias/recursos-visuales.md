# Recursos visuales: textura y movimiento de terceros

Se mira sólo si el brief pide textura o movimiento. Primero va CSS nativo; un recurso de terceros entra con **versión
fija**, **respeto por `prefers-reduced-motion`** y un **respaldo** si falla. Relevado el 2026-10-26 leyendo el código
de cada repositorio (las licencias, comprobadas en su archivo LICENSE); se revisa al usarlo, porque cambian.

## Se usa (con sus condiciones)

| Recurso | Licencia y obligación | Forma de uso | Condiciones | Cuándo sí | Cuándo no |
|---|---|---|---|---|---|
| Paper Shaders, sólo los de textura estática (`paper-texture`, `grain-gradient`, `dithering`, `halftone-dots`) · github.com/paper-design/shaders | Apache 2.0: conservar su NOTICE («Powered by Paper Shaders») | `<script type="module">` desde jsdelivr con versión fija, importando **sólo** el shader que se usa (no `index.js`) | Con `speed=0` no anima. **Si el navegador no tiene WebGL tira un error**: va dentro de `try/catch` con un fondo CSS estático de respaldo, porque la consola tiene que quedar limpia. Está en versión 0.0.x: los cambios pueden romper | Una textura de fondo pedida por el brief, en una página | `MeshGradient` como fondo del hero (es un anti-default); tableros e informes con cifras |
| Desenfoque progresivo en CSS (máscara + `backdrop-filter`), tomado como patrón de motion-primitives (`progressive-blur.tsx`, MIT) | MIT: si se copia código, va el aviso | Se reescribe en CSS, sin la librería | Probar contraste del texto encima | Un borde que se funde sobre una imagen | Glassmorphism decorativo (anti-default) |

## Sólo referencia o descartado

| Recurso | Licencia | Por qué no se usa como dependencia | Qué sirve mirar |
|---|---|---|---|
| awesome-ai-motion · github.com/gongnyang/awesome-ai-motion | MIT, pero trae GSAP con la licencia de GreenSock | Son clips para grabar video, no componentes de página; los clips no respetan el movimiento reducido | Las tablas de tiempos de cada efecto (duración, escalonado, curva) al decidir un movimiento |
| canvas-ui · github.com/DavidHDev/canvas-ui | **MIT + Commons Clause**: no se pueden redistribuir sus componentes, ni portados | Exige TypeScript y bundler; no hay CDN | Sólo se enlaza, nunca se copia; para un efecto de autor en un proyecto con bundler, si el brief lo pide |
| uilayouts · github.com/ui-layouts/uilayouts | MIT en la raíz; hay fragmentos sin origen declarado | React + Tailwind + motion; abundan anti-defaults (carruseles, marquesinas, destellos) | Máscaras con SVG y `clip-path`; sus `design.md` por bloque como modelo de DESIGN.md |
| motion-primitives · github.com/ibelick/motion-primitives | MIT | React + motion, en beta; ningún componente respeta el movimiento reducido (habría que envolverlo) | Patrones sueltos para reescribir en CSS |
| cursify · github.com/ui-layouts/cursify | **Sin licencia**: todos los derechos reservados | No se puede copiar; además, en celular y en pantallas táctiles no hace nada y cambiar el cursor cuesta accesibilidad | Nada |
| superdesign, better-design, design-taste (madebymustafa), taste-skill v2.1.5 | Ver el relevamiento | Skills o apps de diseño que duplican o contradicen las compañeras de `kiln` | Las ideas útiles ya están en `anti-defaults.md` y en el contrato del paso 3 |
| `vaul` · github.com/emilkowalski/vaul | MIT | Su propio `README.md` declara «unmaintained» (push `2025-10-03` al `2026-11-24`) | Usar `<dialog>` nativo o primitivas activas (`Radix` / `Base UI`) |
| `magicui` · github.com/magicuidesign/magicui | MIT | Sus efectos estrella (brillos, rayos, marquesinas) chocan con `anti-defaults.md` | Sólo estudiar un efecto puntual si el brief lo pide explícitamente y respeta `prefers-reduced-motion` |
| `daisyui` · github.com/saadeghi/daisyui | MIT | Temas prearmados de una clase dan estética genérica de plantilla (descartado para AAA con identidad propia) | Prototipos desechables donde la velocidad manda sobre la identidad |
| `cmdk` · github.com/dip/cmdk | MIT | Más de 1 año sin commits (`2025-10-29` al `2026-11-24`) | En `shadcn/ui` ya viene envuelto como `Command`; en HTML/JS puro se resuelve con `<dialog>` + filtro |
| `tremor` · github.com/tremorlabs/tremor | Apache-2.0 | Más de 1 año sin commits (`2025-10-10` al `2026-11-24`) y sus tarjetas KPI de fábrica chocan con `anti-defaults.md` | Ver cómo compone Tailwind + Radix + Recharts; todo tablero sigue sujeto a `datos-en-pantalla.md` |

## Catálogo de referencias AAA (identidad propia, *clean-room*)

Relevado el **2026-11-23**. Regla fija: se estudia la **mecánica, física o jerarquía** para construir una identidad
propia en el contrato del paso 3; nunca se clona el sitio ni se copia código propietario.

### Micro-interacciones, física y widgets (sólo estudio, NO copiar código Pro)

| Referencia | Licencia / estado (`observado`) | Qué estudiar *clean-room* | Límite |
|---|---|---|---|
| [`bencho.dev`](https://bencho.dev) (Lorenzo Cabra) | Comercial / *freemium* (tier gratis explorable; Pro pago ~€79/año o €99 único + MCP propio) | Selects magnéticos, sliders, *dynamic islands*, pickers táctiles, feedback físico y respuestas de estado | No copiar código fuente Pro salvo licencia adquirida; reimplementar el comportamiento en CSS/JS propio |
| [`emilkowal.ski`](https://emilkowal.ski) · [`animations.dev`](https://animations.dev) | Sitio / material educativo de referencia (no librería MIT única) | Curvas `ease-out`, micro-interacciones (`scale: 0.97`), entradas sin *layout shift* y *toasts* | Estudiar principios y temporizaciones; escribir la implementación propia |
| [`rauno.me`](https://rauno.me) | Portfolio y ensayos de design engineering | Calidad táctil, detalles de foco/teclado, transiciones espaciales sobrias | Referencia de oficio; respetar autoría |

### Galerías AAA de dirección visual y estructura (adaptadas al brief)

| Galería | Para qué usarla | Evitar |
|---|---|---|
| [`godly.website`](https://godly.website) | Movimiento editorial, shaders, portadas experimentales con personalidad | Copiar efectos WebGL pesados donde el brief pide lectura o tablero rápido |
| [`awwwards.com`](https://awwwards.com) | Dirección de arte, ritmo de secciones, narrativa y storytelling | Sobre-animación o *scroll hijacking* sin motivo |
| [`siteinspire.com`](https://siteinspire.com) | Grillas editoriales limpias, jerarquía tipográfica y contención | Elegir por estética si choca con densidad operativa del usuario |
| [`a1.gallery`](https://a1.gallery) | Páginas completas y subpáginas (precios, acerca, cabeceras/pies) reales | Armar Frankenstein mezclando bloques de sitios distintos |
| [`mobbin.com`](https://mobbin.com) | Flujos reales de producto, tableros, filtros, ajustes y pantallas móviles | Tratar un flujo de marketing como tablero o viceversa |
| [`onepagelove.com`](https://onepagelove.com) | Referencia curada de páginas únicas, landings y portfolios concretos | Usar estructuras genéricas sin adaptar al verbo del proyecto |

### Primitivas y activos open-source (piezas opcionales; el criterio siempre es de `kiln`)

| Recurso | Condición | Nota |
|---|---|---|
| `tabler/tabler-icons` | MIT (`+5.900` SVGs de trazo limpio) | Íconos por defecto en HTML puro (SVG inline) y en React, evitando emojis y SVGs dibujados a mano |
| [`21st.dev`](https://21st.dev) | **Verificar la licencia individual de cada bloque** antes de incorporar | Útil para gadgets React/Tailwind concretos, siempre re-estilizado con tokens del proyecto |
| `Radix UI` · `Base UI` · `shadcn/ui` | MIT; nunca entregar componentes con estilo de fábrica sin re-tematizar | Usar para comportamiento accesible complejo cuando CSS/HTML nativo (`<dialog>`, `popover`) no alcanza |
| `emilkowalski/sonner` | MIT | *Toasts* apilables con física cuidada en React (en HTML puro se replica con `aria-live="polite"`) |
| `recharts/recharts` | MIT | Gráficos en React cuando SVG nativo no alcanza, siempre sujeto a `datos-en-pantalla.md` |
| `mantinedev/mantine` | MIT; **sistema único** (nunca mezclar con Tailwind/`shadcn`/`Radix`) | Sólo en apps internas o *backoffices* React grandes donde conviene un kit integral (`+120` componentes/hooks) |
