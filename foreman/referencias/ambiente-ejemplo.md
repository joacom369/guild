# Configuración del ambiente (plantilla común)

Esta plantilla es la **única dueña** de dónde vive la configuración del ambiente y dónde están sus registros. Los
oficios que necesitan configuración propia (por ejemplo, `sherpa`) agregan su bloque **en el mismo archivo**.

Se busca, en este orden:
1. `~/.foreman/ambiente.md`;
2. el archivo de reglas del ambiente (CLAUDE.md, AGENTS.md o el que use la plataforma).

Va fuera del repositorio de skills: es propia de cada trabajo y de cada persona. Si no hay configuración, valen los
valores por defecto.

```markdown
## foreman · <nombre del trabajo>

- Modo por defecto: propone            # charla | propone | tramo
- Proyectos (nombre → carpeta):
  - <Nombre del proyecto> → <ruta>
- Skills de dominio del ambiente: <nombres>, se cargan antes de cada fase que toque sus sistemas
- Detección de tareas repetidas: <qué historial ofrece esta plataforma>; siempre con permiso previo
- Registros (si no se dice otra cosa, los de la tabla de abajo)
- Bloques de oficios en otro archivo: <ruta> (si el bloque de un oficio, como el de `sherpa`, vive aparte)
- Autorizaciones permanentes acotadas (`herald`): <destino · tipo de contenido · fecha en que el usuario lo autorizó>

## <oficio> · <nombre del trabajo>
- … el bloque de cada oficio que lo pida (la plantilla está en su skill)
```

## Registros y valores por defecto

| Qué | Por defecto | Lo escribe |
|---|---|---|
| Modo | `propone` | — |
| Buzón de ideas | `~/.foreman/IDEAS.md` | `foreman` |
| Registro de lentes | `~/.foreman/LENTES.md` | `lenses` |
| Registro de delegaciones | `~/.foreman/DELEGACIONES.md` | `foreman` (con la ficha de `tokenwise`) |
| Registro de escrituras | `~/.foreman/ESCRITURAS.md` | `herald` |
| Registro de automatizaciones | `~/.foreman/AUTOMATIZACIONES.md` | `foundry`; `foreman` mira las mediciones vencidas |
| Estado de cada proyecto | `ESTADO.md` en la raíz del proyecto | `foreman` (la plantilla es de `provenance`) |

Todo fuera de los proyectos y del repositorio de skills, salvo el estado: es personal y no ensucia nada. Si un archivo
no existe, se crea la primera vez que hace falta escribir en él.

## Formato del buzón

```markdown
| Fecha | Área | Idea | Por qué importa | Estado (nueva / charlada / aprobada / aplicada / descartada) |
|---|---|---|---|---|
```

## Lo que necesita un adaptador

El núcleo pide que **al empezar una conversación** se revisen el buzón, las mediciones vencidas y el estado del
proyecto, y que se avise en una línea si hay novedades. Una skill sola no corre al abrir la sesión; cada plataforma
lo resuelve a su manera (un hook de inicio, su mecanismo de reglas o de arranque). Los adaptadores están en
`adaptadores/` del repositorio de skills. Instalar un adaptador es decisión del usuario.
