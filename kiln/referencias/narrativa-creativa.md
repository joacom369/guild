# Narrativa creativa con datos

Cómo pasar de «datos en cajas» (grillas Bento uniformes y gráficos pasivos) a instrumentos y objetos propios del dominio, en donde la forma visual vuelve legible la estructura matemática sin maquillarla.

Aplica en primer lugar a **entregables interactivos** (HTML, tableros vivos, simuladores) y se ofrece como **opción explícita al usuario** en documentos y presentaciones estáticas (ver [archivos.md](archivos.md)).

## 1. Del gráfico genérico al objeto del dominio

Antes de dibujar tarjetas o barras estándar, buscar qué artefacto físico o geométrico representa la mecánica central del problema:

| Área | Reemplaza la grilla genérica por… | Qué vuelve legible |
|---|---|---|
| **Finanzas personales** | Frasco graduado contra meta de meses, billete doblado por destino del ingreso, cuota nominal frente a cuota licuada dentro del mismo marco | Margen real, composición del flujo y efecto de la inflación sobre obligaciones fijas |
| **Macroeconomía** | Balanza fiscal o externa en tensión, corredor o banda cambiaria/inflacionaria, pronóstico enganchado a los supuestos del escenario | Vínculo causal entre régimen, shock nominal y resultado real |
| **Microeconomía** | Curvas de oferta/demanda o elasticidad manipulables en línea, frontera de eficiencia interactiva | Qué cambia el excedente o el óptimo al mover un precio o costo |
| **Econometría y estadística** | Abanico Monte Carlo reproducible conectado a grilla 10×10 (1 celda = 1 % de corridas), torneo fuera de muestra (RMSE/sesgo con barras clicables), tornado con botón «Probar borde» | Asimetría entre media, mediana y determinista; cercanía real entre modelos competidores; umbrales de quiebre |
| **Marketing y negocio** | Embudo manipulable paso a paso, matriz precio × retención donde tocar una celda recalcula todo, cohorte viva | Palancas de conversión, elasticidad y zona de equilibrio |

## 2. Cuatro mecánicas interactivas probadas

- **Prosa manipulable en línea (*Tangle*):** poner los supuestos clave como valores arrastrables (`ew-resize` + teclado `←`/`→`, `role="spinbutton"`) dentro de la frase que resume la conclusión, sincronizados bidireccionalmente con diales y gráficos.
- **Instrumento unificado sobre el mismo eje:** alinear trayectoria, banda de incertidumbre y desglose mensual debajo del mismo eje horizontal. Cuando cualquier período o neto cruza a negativo, trazar una **línea cero real** visible y colgar las barras de déficit hacia abajo.
- **Capas conectadas («Lentes») en análisis profundos:** cuando hay varios bloques densos (Monte Carlo, serie de inflación, tornado, matriz, hitos), ordenarlos en pestañas o lentes atadas al **mismo estado** en lugar de apilar una sábana pasiva. Tocar un modelo competidor, una celda de la matriz o un botón de quiebre inyecta ese valor en el instrumento principal y actualiza todo en el acto.
- **Enmascarado selectivo de privacidad (`.monto`):** si la interfaz incluye modo ocultar montos, ocultar únicamente cifras monetarias (en HTML y en `<text>` SVG), manteniendo legibles porcentajes, `p`-valores, `RMSE` y prosa causal.

## 3. Registro flexible según el encargo

Elegir en el contrato del paso 3 el tono y nivel de detalle según quién lee:

- **Ejecutivo:** síntesis inmediata, una figura dominante por vista, conclusiones y palancas accionables arriba; el detalle técnico queda en capa secundaria o diálogo bajo demanda.
- **Editorial:** columna narrativa guiada, títulos con la conclusión, objetos tangibles y transiciones suaves que explican un mecanismo causal por paso.
- **Académico / econométrico:** supuestos, tests de diagnóstico (`ADF`, `KPSS`, `RMSE`, sesgo), semilla reproducible y controles deterministas a la vista junto a la exploración.
- **Operativo:** controles directos de baja fricción, atajos de teclado, estados extremos y límites resaltados sin texto de relleno.

## 4. Extensión opcional a entregas estáticas

En informes escritos, presentaciones o PDFs que comunican análisis cuantitativo, proponer al usuario antes de construir la opción de trasladar estas piezas al formato estático (grilla 10×10 para frecuencias, billete o diagrama de flujo proporcional, comparador visual de modelos, llamadas directas sobre la serie), verificando siempre el contraste y la lectura al exportarse a imagen o papel.

## 5. Guardarraíl (`provenance` + `ponytail`)

- **Rigor antes que adorno:** creatividad para hacer visible el mecanismo del modelo, nunca para ocultar incertidumbre ni suavizar quiebres.
- **Semilla y control en sorteos:** toda simulación aleatoria usa semilla reproducible y muestra su control contra la media teórica o el caso determinista.
- **Escenario, nunca profecía:** las perillas y celdas simuladas se rotulan como `escenario`, distinguiéndolas de datos `observados` o `calculados`.
- **Estados extremos honestos:** el cero, el déficit y el dato ausente se dibujan explícitamente sin falsos porcentajes negativos ni pisos cortados sin aviso.
- **Código mínimo:** preferir SVG, CSS y JavaScript nativos antes que librerías de gráficos pesadas si no hacen falta.
