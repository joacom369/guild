# Configuración del ambiente para sherpa (plantilla)

Este bloque va en el archivo de configuración del ambiente que fija la plantilla común de `foreman`
(`~/.foreman/ambiente.md` o el archivo de reglas), o en el encargo de la rutina programada. **No lo completes dentro
de la skill:** la skill es igual para cualquier trabajo.

```markdown
## sherpa · <nombre del trabajo>

- Usuario: <nombre>
- Horario laboral (zona <IANA, p. ej. America/Argentina/Buenos_Aires>):
  - lunes <hh:mm–hh:mm>
  - …
- Fuentes (una por línea; cada una con su cuenta verificada y la fecha):
  - chat · <Slack / Teams> · conector <cuál> · cuenta <ID o @usuario>, verificada el <fecha>
    - novedades: menciones al usuario y a <@equipo (ID del grupo)>, mensajes directos, hilos donde participó,
      canales <todos | lista | prefijos>
  - correo · <Gmail / Outlook> · conector <cuál> · cuenta <dirección>, verificada el <fecha>
    - novedades: correos sin responder dirigidos al usuario; respuestas a lo que el usuario preguntó
  - calendario · conector <cuál> · calendario <id>, verificado el <fecha>
    - novedades: reuniones de hoy y de la semana, invitaciones sin responder
  - <otra fuente> · conector <cuál> · cuenta <…>, verificada el <fecha>
    - novedades: <qué cuenta como novedad: ticket asignado, PR que espera revisión, estado que cambió…>
- Tope por corrida: <«sin tope» en lo dirigido al usuario o a su grupo | N ítems>; para contexto, hasta <N> hilos o
  ítems relacionados por pendiente (si se supera, decir qué quedó sin leer)
- Urgente es: <clientes clave, plazos del día, sistemas caídos, palabras como «urgente», «hoy», «bloqueado»>
- Skill de dominio con el criterio del área: <nombre, si existe>
- Entrega en corrida programada: la autorización permanente acotada de `herald` (<destino>, autorizada el <fecha>)
```

El ID de un grupo es el que aparece en las menciones (por ejemplo `<!subteam^S0…>` en Slack), no su nombre.
