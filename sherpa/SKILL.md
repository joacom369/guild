---
name: sherpa
description: Pone al usuario en contexto al empezar su jornada. Lee lo que pasó en el chat del trabajo (menciones a él o a su grupo, mensajes directos, canales de su zona) y, si hace falta, en su correo; lo clasifica en urgente, pendiente suyo, contexto y ruido; y entrega un resumen corto con enlaces, con lo descartado a la vista y conteos que cierran. Funciona con cualquier chat y correo (Slack, Teams, Gmail, Outlook) según la configuración del ambiente. Usar cuando el usuario pide ponerse al día («¿qué me perdí?», «revisá mis notificaciones», «resumen de Slack»), al empezar la jornada, o con /sherpa. No responde mensajes, no marca nada como leído y no publica en canales; sólo lee y entrega el resumen. Tampoco diseña ni automatiza esta revisión; si el usuario quiere automatizar su repaso diario del chat o del correo, es `foundry`.
argument-hint: "[desde cuándo, si no es la jornada anterior]"
---

# Sherpa: el que lleva la carga y te pone en contexto

El sherpa conoce la montaña y carga lo pesado para que el otro llegue con aire. Esta skill lee todo lo que pasó desde
la última jornada y le entrega al usuario **lo que tiene que saber y lo que le toca hacer**, en una pantalla.

## Las reglas (no se negocian)

1. **Primero la identidad, fuente por fuente.** Antes de leer un solo mensaje, verificá que la cuenta de **cada**
   conector (chat, correo, calendario) sea la del usuario configurado: que una sea suya no dice nada de las otras. La
   que no coincide **no se lee** y se avisa arriba de todo: leer la cuenta de otra persona expone sus conversaciones
   privadas. Cómo conseguir un conector propio: [referencias/conectores.md](referencias/conectores.md).
2. **Sólo lectura.** No responde, no reacciona, no marca como leído, no archiva. La única escritura permitida es
   **entregar el resumen** en el destino que el usuario autorizó en la configuración.
3. **Nada se descarta en silencio.** Lo que se clasifica como ruido aparece en una lista plegada al final. Ante la
   duda entre dos categorías, va a la más alta.
4. **Los conteos cierran:** leídos = urgentes + pendientes + contexto + ruido. Si no cierran, se dice.
5. **Una fuente que falla va arriba de todo.** «No pude leer el correo» es lo primero que se lee, no una nota al pie.

## La configuración del ambiente

Todo lo propio de un trabajo (qué chat, qué usuario, qué grupos, qué es urgente, dónde entregar) vive **fuera de
esta skill**, en un archivo de ambiente o en el encargo de la rutina programada. Plantilla en
[referencias/ambiente-ejemplo.md](referencias/ambiente-ejemplo.md). Si falta la configuración y la sesión es
interactiva, se pide; si es una corrida programada, se entrega un resumen que dice que falta y se termina.

## El procedimiento

1. **Ventana.** Desde el inicio de la jornada anterior según el horario configurado (o lo que pida el usuario). Se
   dice al principio del resumen: «Desde el viernes 16:00 hasta hoy 9:00».
2. **Identidad** (regla 1): el perfil de cada cuenta conectada contra el usuario configurado.
3. **Recolectar**, con búsquedas filtradas por fecha antes que leyendo canal por canal (son cientos):
   - menciones al usuario y a sus grupos o alias;
   - mensajes directos y grupales;
   - hilos donde el usuario participó y tuvieron respuestas nuevas;
   - actividad en los canales de su zona (todos, si así está configurado). Si el volumen supera el tope configurado,
     se priorizan los canales con más actividad y **se dice qué canales quedaron sin leer**;
   - si hay calendario, las reuniones de hoy y de la semana, y las invitaciones sin responder.

   **Control positivo.** Antes de concluir «0 menciones», probá la búsqueda con una mención que sabés que existe: las
   plataformas suelen guardar la mención como un ID (del usuario o del grupo), no como el nombre. Sin ese control, el
   resultado va como «no verificado». Los resúmenes anteriores de la propia `sherpa` no se cuentan.
4. **Clasificar** cada mensaje o hilo:

   | Categoría | Criterio |
   |---|---|
   | **Urgente** | Coincide con una alarma de la configuración (cliente afectado, plazo hoy, algo caído), o lo pide alguien con un plazo vencido |
   | **Pendiente tuyo** | Una pregunta o un pedido dirigido al usuario o a su grupo, sin respuesta de él todavía |
   | **Contexto** | No le pide nada, pero cambia algo de su trabajo: una decisión, un precio, un estado, un cliente de su zona |
   | **Ruido** | Saludos, anuncios generales, conversaciones ajenas a su zona |

   Si el criterio de urgencia del área está escrito en una skill de dominio, se usa esa.
5. **Una sola línea de tiempo.** Ordená el chat y el correo juntos, por tema (cliente, pedido, proyecto): un pedido
   del chat puede quedar resuelto por correo minutos después, y entonces ya no es pendiente. Cuando un mensaje pregunta
   si alguien contestó un correo («¿respondió el proveedor X?»), se busca en el correo del usuario, sólo lectura, y se
   agrega el estado («respondió el 24/10: …» o «sin respuesta desde el 20/10»). Para dar contexto a un pendiente se
   leen el hilo, el canal y los correos del tema, hasta el tope de contexto configurado.
6. **Armar el resumen**, pensado para leerse en el celular:
   1. Ventana, qué fuentes se leyeron y, si las hubo, fallas de lectura.
   2. **Hoy y esta semana** (si hay calendario): reuniones con hora, y las invitaciones sin responder.
   3. **Urgente**: una línea por ítem, con quién, qué pide y el enlace.
   4. **Pendientes tuyos**, igual, ordenados por antigüedad.
   5. **Contexto**, agrupado por cliente, oportunidad o tema; una o dos líneas por grupo. Incluye lo que el usuario
      preguntó y todavía espera.
   6. **Ruido**: la cuenta y la lista plegada.
   7. Conteos: leídos = urgentes + pendientes + contexto + ruido.

   Si pasa de una pantalla, se recorta el contexto, nunca lo urgente ni los pendientes.
7. **Entregar:** en la sesión, en el chat; en una corrida programada, en el destino configurado (por ejemplo, un
   mensaje privado al propio usuario). Nada más se escribe.

## Lo que no hace (todavía)

Buscar la información para resolver cada pendiente y dejar un borrador de respuesta. Es la opción C del diseño en
`foundry`: se suma cuando la versión actual demuestre que no se le escapa nada.

## Cómo se combina

- Nació en `foundry` (registro en `mapa/AUTOMATIZACIONES.md`).
- Las skills de dominio del ambiente dan el criterio de urgencia y el vocabulario.
- `hallmark` si el resumen lleva cifras que hay que verificar.
