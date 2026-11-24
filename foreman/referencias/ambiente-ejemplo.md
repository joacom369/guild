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

La taxonomía de memoria (`Semántica`, `Episódica`, `Procedural`) y su higiene viven en `provenance` (`referencias/registro-y-comunicacion.md`).

| Qué | Por defecto | Memoria | Lo escribe |
|---|---|---|---|
| Modo | `propone` | Semántica | — |
| Buzón de ideas | `~/.foreman/IDEAS.md` | Procedural | `foreman` |
| Registro de lentes | `~/.foreman/LENTES.md` | Episódica | `lenses` |
| Registro de delegaciones | `~/.foreman/DELEGACIONES.md` | Episódica | `foreman` (con la ficha de `tokenwise`) |
| Registro de escrituras | `~/.foreman/ESCRITURAS.md` | Episódica | `herald` |
| Registro de automatizaciones | `~/.foreman/AUTOMATIZACIONES.md` | Episódica / Predicción | `foundry`; `foreman` mira las mediciones vencidas |
| Estado de cada proyecto | `ESTADO.md` en la raíz del proyecto | Semántica + Episódica | `foreman` (la plantilla es de `provenance`) |

Todo fuera de los proyectos y del repositorio de skills, salvo el estado: es personal y no ensucia nada. Si un archivo
no existe, se crea la primera vez que hace falta escribir en él.

## Formato del buzón

```markdown
| Fecha | Área | Idea | Por qué importa | Estado (nueva / charlada / aprobada / aplicada / descartada) |
|---|---|---|---|---|
```

Una idea **descartada** lleva su motivo en el estado («descartada: licencia no abierta»). No se vuelve a proponer
salvo que aparezca un hecho nuevo que cambie ese motivo; así el buzón también es el registro de lo que ya se
evaluó.

## Lo que necesita un adaptador

El núcleo pide que **al empezar una conversación** se revisen el buzón, las mediciones vencidas y el estado del
proyecto, y que se avise en una línea si hay novedades. Una skill sola no corre al abrir la sesión; cada plataforma
lo resuelve a su manera (un hook de inicio, su mecanismo de reglas o de arranque). Los adaptadores están en
`adaptadores/` del repositorio de skills. Instalar un adaptador es decisión del usuario.

## Observabilidad estructurada (opt-in)

Si un adaptador agrega una traza JSONL de sesiones o herramientas, no se habilita por defecto y exige cuatro condiciones previas:
1. **Emisor explícito:** definir en el adaptador qué hook (p. ej. post-herramienta o cierre de turno) escribe la traza.
2. **Filtro de privacidad:** registrar evento, timestamp, modelo, oficio y estado/duración sin guardar prompts completos, secretos ni datos privados de otros frentes.
3. **Codificación explícita:** UTF-8 sin BOM también en Windows.
4. **Lectura con permiso:** inspeccionar trazas históricas sigue pidiendo aprobación previa al usuario (`foreman` regla 6, declarando qué se lee y cuánto cuesta).
