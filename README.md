# Skills de Claude

Skills propias para Claude Code. Viven en `~/.claude/skills/`, que es este mismo
repositorio: se editan ahí y se suben con commit y push.

| Skill | Para qué |
|---|---|
| `provenance` | Forma de pensar para trabajos con datos, modelos y decisiones: origen y estado de cada cifra, validación, hábitos para no casarse con un supuesto. |
| `kiln` | Frontend pulido desde el primer intento: entiende qué busca el usuario, ofrece direcciones con vista previa, fija un contrato de diseño, construye con código mínimo y se mira en escritorio y celular antes de mostrar. Deriva el pulido a `impeccable` y `design-taste-frontend`. |
| `tokenwise` | Cómo repartir tareas entre subagentes con la mejor calidad al menor costo de tokens; equipos de especialistas sólo con aval del usuario. |
| `criterio-herramientas` | Elegir la técnica o herramienta (estadística, econometría, espacial, ML, BI) que conviene para una pregunta, y decir cuándo no conviene. |

## De terceros

Copias sin modificar, versionadas para tenerlas en cualquier PC. Cada una conserva su licencia.

| Skill | Autor y licencia | Para qué |
|---|---|---|
| `impeccable` | Paul Bakaus, Apache 2.0 (github.com/pbakaus/impeccable), v4.5.0 | Diseñar, pulir y auditar interfaces. |
| `design-taste-frontend` | Leonxlnx (taste-skill), MIT | Dirección visual que no parezca plantilla al construir una página. |

Para actualizarlas, reemplazar la carpeta entera por la versión nueva del autor; no editarlas acá.

## Instalar

**Desde Claude Code (cualquier PC, desde el chat):**

```
/plugin marketplace add joacom369/claude-skills
/plugin install kiln@joaco-skills
```

Lo mismo con `provenance`, `tokenwise`, `impeccable` o `design-taste-frontend`. El repositorio es privado: la PC
tiene que tener acceso a GitHub con tu cuenta (por ejemplo, `gh auth login`).

**Desde claude.ai (el chat web o de escritorio):** descargar `dist/<skill>.zip` de este repositorio y subirlo en
Configuración > Capacidades > Skills. En claude.ai los scripts corren en su propio entorno: `kiln/scripts/foto_pagina.py`
necesita un Chrome local y sólo funciona en Claude Code.

Después de editar una skill propia, regenerar los ZIP con `python empaquetar.py` antes del commit.

## Instalar en otra PC (clonando)

```bash
git clone https://github.com/joacom369/claude-skills.git ~/.claude/skills
```

Si `~/.claude/skills` ya existe, clonar aparte y copiar las carpetas.
