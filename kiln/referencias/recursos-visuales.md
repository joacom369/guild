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
