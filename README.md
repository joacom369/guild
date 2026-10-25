# Skills de Claude

Skills propias para Claude Code. Viven en `~/.claude/skills/`, que es este mismo
repositorio: se editan ahí y se suben con commit y push.

| Skill | Para qué |
|---|---|
| `provenance` | Forma de pensar para trabajos con datos, modelos y decisiones: origen y estado de cada cifra, validación, hábitos para no casarse con un supuesto. |
| `kiln` | Frontend pulido desde el primer intento: entiende qué busca el usuario, ofrece direcciones con vista previa, fija un contrato de diseño, construye con código mínimo y se mira en escritorio y celular antes de mostrar. Deriva el pulido a `impeccable` y `design-taste-frontend`. |
| `tokenwise` | Cómo repartir tareas entre subagentes con la mejor calidad al menor costo de tokens; equipos de especialistas sólo con aval del usuario. |
| `compass` | Elegir la técnica o herramienta (estadística, econometría, espacial, ML, BI) que conviene para una pregunta, y decir cuándo no conviene. |
| `quarry` | Sacar datos de cualquier origen (SQL, API, MCP, planillas, web) sin romper la fuente: estimar, muestra, foto con ficha y hash, perfil al llegar (nulos aparte de ceros, claves, cruces). Scripts en Python. |
| `foundry` | Taller que convierte una tarea repetida en una automatización: relevamiento, cuenta de si vale la pena, búsqueda en el árbol, lentes que proponen por separado, opciones en una escalera de siete escalones y registro con predicción medible. |
| `sherpa` | Pone al usuario en contexto al empezar la jornada: lee chat y correo, clasifica en urgente, pendiente, contexto y ruido, y entrega un resumen corto con lo descartado a la vista. Sólo lectura; verifica la identidad de la cuenta antes de leer. Primera automatización salida de `foundry`. |
| `assay` | Analizar o modelar con salidas reproducibles: plan antes de ver resultados, pre-análisis, cálculo en una corrida con su ficha (entradas verificadas, semilla, versión), todos los intentos contados, protocolo de modelado y sensibilidad. Script en Python. |
| `hallmark` | Control ejecutable antes de entregar: cada cifra del entregable buscada en las salidas, identidades que cierran, lectura como la ve el lector, revisión independiente y acta. Scripts en Python. |

## De terceros

Copias sin modificar, versionadas para tenerlas en cualquier PC. Cada una conserva su licencia.

| Skill | Autor y licencia | Para qué |
|---|---|---|
| `impeccable` | Paul Bakaus, Apache 2.0 (github.com/pbakaus/impeccable), v4.5.0 | Diseñar, pulir y auditar interfaces. |
| `design-taste-frontend` | Leonxlnx (taste-skill), MIT | Dirección visual que no parezca plantilla al construir una página. |

Para actualizarlas, reemplazar la carpeta entera por la versión nueva del autor; no editarlas acá.

## Instalar

**Desde Claude Code (cualquier PC, desde el chat), una línea por skill:**

```
/plugin install kiln --marketplace joacom369/claude-skills
/plugin install provenance --marketplace joacom369/claude-skills
/plugin install tokenwise --marketplace joacom369/claude-skills
/plugin install compass --marketplace joacom369/claude-skills
/plugin install quarry --marketplace joacom369/claude-skills
/plugin install assay --marketplace joacom369/claude-skills
/plugin install hallmark --marketplace joacom369/claude-skills
/plugin install foundry --marketplace joacom369/claude-skills
/plugin install sherpa --marketplace joacom369/claude-skills
/plugin install impeccable --marketplace joacom369/claude-skills
/plugin install design-taste-frontend --marketplace joacom369/claude-skills
```

En versiones de Claude Code anteriores a la 2.1.275, primero `/plugin marketplace add joacom369/claude-skills` y después
`/plugin install <skill>@joaco-skills`. El repositorio es privado: la PC tiene que tener acceso a GitHub con tu cuenta
(por ejemplo, `gh auth login`).

**Desde claude.ai (el chat web o de escritorio):** descargar `dist/<skill>.zip` de este repositorio y subirlo en
Configuración > Capacidades > Skills. En claude.ai los scripts corren en su propio entorno: `kiln/scripts/foto_pagina.py`
necesita un Chrome local y sólo funciona en Claude Code. Los scripts de `quarry`, `assay` y `hallmark` usan la biblioteca
estándar de Python (más `openpyxl` para `.xlsx`) y corren en los dos lados.

Después de editar una skill propia, regenerar los ZIP con `python empaquetar.py` antes del commit.

## Instalar en otra PC (clonando)

```bash
git clone https://github.com/joacom369/claude-skills.git ~/.claude/skills
```

Si `~/.claude/skills` ya existe, clonar aparte y copiar las carpetas.
