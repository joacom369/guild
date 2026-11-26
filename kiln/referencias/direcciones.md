# Catálogo de direcciones

Para ofrecer opciones en el paso 2. Cada dirección es un punto de partida, no una plantilla: el contrato la
ajusta al pedido. Ofrecé las 2 a 4 que encajan, no las seis.

| Si el usuario busca… | Dirección | Rasgos | Evita |
|---|---|---|---|
| Contar algo con datos (informe, ensayo, resultados) | **Editorial narrativa** | Columna de lectura de 60–75 caracteres, títulos que dicen la conclusión, una figura dominante por sección, cifras como tipografía, avance con el scroll | Grilla de tarjetas, contadores animados, gráficos decorativos |
| Operar o monitorear (tablero, panel interno) | **Tablero denso** | Cuadrícula estable, cifras con unidad y comparación, filtros persistentes, tablas fuertes, color sólo para estado | Hero, ilustraciones, animación que distrae, colores por adorno |
| Vender o convencer (landing, servicio, campaña) | **Producto con una idea** | Portada partida (texto e imagen real del producto), una sola llamada a la acción, prueba concreta (cifras, clientes, capturas), ritmo de secciones distintas | Tres tarjetas iguales con ícono, gradiente violeta, mockups genéricos |
| Transmitir confianza (institucional, regulado, público amplio) | **Sobria y accesible** | Contraste alto, tipografía legible, poco movimiento, jerarquía clara, formularios cuidados | Efectos, texto sobre imagen, letra chica |
| Sorprender o mostrar un espacio (gemelo, recorrido, producto físico) | **Inmersiva / 3D** | Escena con una cámara con intención, recorrido guiado por pasos, panel de datos sobrio al costado, versión sin 3D para celulares débiles | 3D por el efecto, controles sin guía, cargar todo de golpe |
| Mostrar trabajo (portfolio, galería, caso) | **Vitrina** | La obra manda desde la primera pantalla, la interfaz se retira, tipografía con carácter | Texto que compite con la obra |
| Explorar un modelo, escenario o datos complejos (finanzas, macro, micro, econometría, marketing) | **Instrumento vivo** | Prosa manipulable, objetos tangibles del dominio, capas conectadas al mismo estado, registro elegido según el encargo ([narrativa-creativa.md](narrativa-creativa.md)) | Grilla Bento de tarjetas sueltas, gráficos pasivos desconectados, adorno sin dato |

## Cómo armar la vista previa de cada opción

Un boceto ASCII del primer viewport (10 a 15 líneas) y una línea con paleta y tipografía. Ejemplo:

```
┌──────────────────────────────────────────┐
│ Título que dice la conclusión            │
│ Bajada de una línea                      │
│                                          │
│ ███████████████  figura dominante        │
│ ███████████████                          │
│ Fuente · unidad · fecha                  │
└──────────────────────────────────────────┘
Fondo blanco roto frío · tinta casi negra · un acento verde · títulos grotesca, cifras tabulares
```

## Vista previa en imagen antes de construir (páginas nuevas o grandes)

Para ajustes chicos alcanza el boceto ASCII. En **páginas nuevas, landings, portfolios o tableros grandes** (o cuando
el usuario pide ver el rumbo antes de programar todo), mostrar una vista previa en imagen y esperar confirmación
(«me gusta» o qué cambiar) antes de construir el entregable completo:

- **Por defecto — *Style tile* o primer viewport real en HTML+CSS + captura:** armar una pieza mínima con los `:root`
  tokens reales, la tipografía real y `1` widget/gadget representativo, capturarla con `foto_pagina.py` (o render
  inline) y mostrársela al usuario. Todo lo que aprueba es 100% reproducible y queda como base del código final.
- **Opcional — *Moodboard* conceptual (`image-generator`, si existe en la plataforma):** usar sólo cuando el brief es
  muy artístico, editorial o 3D y conviene explorar clima y composición rápido antes de escribir CSS. Aclarar siempre
  que la imagen generada es referencia de atmósfera/paleta y no plano literal de tipografía ni de píxeles.

## Perillas para afinar (después de elegir)

- **Densidad:** aireada · media · compacta.
- **Movimiento:** quieto · transiciones · narrativo (scroll) · cinematográfico.
- **Tono:** sobrio · cálido · técnico · expresivo.
- **Registro (en entregas con datos):** ejecutivo · editorial · académico · operativo (ver [narrativa-creativa.md](narrativa-creativa.md)).

Ofrecelas como segunda pregunta sólo si la primera no las resolvió.
