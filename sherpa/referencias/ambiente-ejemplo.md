# Configuración del ambiente para sherpa (plantilla)

Copiá este bloque al archivo de reglas del ambiente (CLAUDE.md, AGENTS.md o el que use la plataforma), a un archivo propio fuera del repositorio de skills, o al encargo de la
rutina programada. **No lo completes dentro de la skill:** la skill es igual para cualquier trabajo.

```markdown
## sherpa · <nombre del trabajo>

- Usuario: <nombre> · chat: <Slack / Teams> usuario <ID o @usuario> · correo: <dirección>
- Conectores (cada uno con su cuenta verificada y la fecha): chat <cuál> · correo <cuál> · calendario <cuál o «no»>
- Grupos o alias que también lo nombran: <@equipo (ID del grupo), @area (ID)>; el ID es el que aparece en las menciones
- Canales: <todos | lista | prefijos>
- Tope por corrida: <«sin tope» en lo dirigido al usuario o a su grupo | N mensajes>; para contexto, hasta <N> hilos,
  canales o correos por pendiente (si se supera, decir qué quedó sin leer)
- Horario laboral (zona <IANA, p. ej. America/Argentina/Buenos_Aires>):
  - lunes <hh:mm–hh:mm>
  - …
- Urgente es: <clientes clave, plazos del día, sistemas caídos, palabras como «urgente», «hoy», «bloqueado»>
- Skill de dominio con el criterio del área: <nombre, si existe>
- Entrega en corrida programada: <mensaje privado a uno mismo | otro destino> (autorizado por el usuario el <fecha>)
```
