---
description: "Vuelta de automejora del gremio. Usar cuando arranca la rutina, cuando el usuario pide revisar mejoras, o cuando hay que proponer cómo trabajar mejor. No edita skills, instrucciones ni archivos del repositorio, y no manda mensajes afuera (eso es herald)."
---

# Automejora

Cada propuesta espera aprobación. Registrar no es aplicar.

1. Llamá a `listar_propuestas`.
2. Llamá a `correr_auditor_gremio`. Si `disponible` es falso, decilo y seguí con el diario de memoria. Si está, corré también con `dinamico: true` sólo cuando el reporte estático ya se leyó.
3. Por cada aviso nuevo del reporte, una propuesta:
   - `comun` si el hueco aparece en más de un oficio o el encargo se repite;
   - `puntual` si es de un solo oficio, y `area` es el nombre de ese oficio;
   - `resultado` si es un tramo que queda abierto o una medición vencida.
4. `registrar_propuesta` con título corto, por qué importa y la evidencia (archivo o fila). Si responde `ya estaba`, no la repitas.
5. Respondé con las propuestas nuevas y el total. La primera línea dice que ninguna skill se editó.
