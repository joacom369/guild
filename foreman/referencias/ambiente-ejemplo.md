# Configuración del ambiente para foreman (plantilla)

Se busca, en este orden, en `~/.foreman/ambiente.md` y en el archivo de reglas del ambiente (CLAUDE.md,
AGENTS.md o el que use la plataforma). Va fuera del repositorio de
skills. Si no hay configuración, valen los valores por defecto.

```markdown
## foreman · <nombre del trabajo>

- Modo por defecto: propone            # charla | propone | tramo
- Buzón de ideas: ~/.foreman/IDEAS.md  # ideas sobre el sistema y las herramientas; vale para todos los proyectos
- Registro de lentes: ~/.foreman/LENTES.md
- Estado de cada proyecto: ESTADO.md en la raíz del proyecto
- Proyectos (nombre → carpeta):
  - <Nombre del proyecto> → <ruta>
- Skills de dominio del ambiente: <nombres>, se cargan antes de cada fase que toque sus sistemas
- Detección de tareas repetidas: <qué historial ofrece esta plataforma>; siempre con permiso previo
```

## Valores por defecto

| Qué | Por defecto | Por qué ahí |
|---|---|---|
| Modo | `propone` | Las decisiones de método son del usuario |
| Buzón | `~/.foreman/IDEAS.md` | Fuera de los proyectos y del repositorio de skills: es personal y no ensucia nada |
| Registro de lentes | `~/.foreman/LENTES.md` | Igual que el buzón |
| Estado | `ESTADO.md` en la raíz del proyecto | Viaja con el proyecto |

Si un archivo no existe, se crea la primera vez que hace falta escribir en él.

## Formato del buzón

```markdown
| Fecha | Área | Idea | Por qué importa | Estado (nueva / charlada / aprobada / descartada) |
|---|---|---|---|---|
```

## Lo que necesita un adaptador

El núcleo pide que **al empezar una conversación** se revisen el buzón y el estado del proyecto, y que se avise en una
línea si hay novedades. Una skill sola no corre al abrir la sesión; cada plataforma lo resuelve a su manera:
- **Claude Code:** un hook de inicio de sesión que lea el buzón y muestre la línea, y una línea en el CLAUDE.md que
  diga cuándo llamar a `foreman`;
- **otras plataformas:** su mecanismo de reglas o de arranque.

Los adaptadores de cada plataforma están en `adaptadores/` del repositorio.

Instalar un adaptador es decisión del usuario.
