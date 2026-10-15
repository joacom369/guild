# Skills de Claude

Skills propias para Claude Code. Viven en `~/.claude/skills/`, que es este mismo
repositorio: se editan ahí y se suben con commit y push.

| Skill | Para qué |
|---|---|
| `provenance` | Forma de pensar para trabajos con datos, modelos y decisiones: origen y estado de cada cifra, validación, hábitos para no casarse con un supuesto. |
| `tokenwise` | Cómo repartir tareas entre subagentes con la mejor calidad al menor costo de tokens; equipos de especialistas sólo con aval del usuario. |

## De terceros

Copias sin modificar, versionadas para tenerlas en cualquier PC. Cada una conserva su licencia.

| Skill | Autor y licencia | Para qué |
|---|---|---|
| `impeccable` | Paul Bakaus, Apache 2.0 (github.com/pbakaus/impeccable), v4.5.0 | Diseñar, pulir y auditar interfaces. |
| `design-taste-frontend` | Leonxlnx (taste-skill), MIT | Dirección visual que no parezca plantilla al construir una página. |

Para actualizarlas, reemplazar la carpeta entera por la versión nueva del autor; no editarlas acá.

## Instalar en otra PC

```bash
git clone https://github.com/joacom369/claude-skills.git ~/.claude/skills
```

Si `~/.claude/skills` ya existe, clonar aparte y copiar las carpetas.
