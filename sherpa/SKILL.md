---
name: sherpa
description: >
  Pone al usuario en contexto al empezar su jornada. Lee lo que pasó en las fuentes que el usuario conectó (el chat
  del trabajo, el correo, el calendario y cualquier otra que declare: tickets, CRM, repositorios, un sistema interno),
  lo ordena en una sola línea de tiempo, lo clasifica en urgente, pendiente suyo, contexto y ruido, y entrega un
  resumen corto con enlaces, con lo descartado a la vista y conteos que cierran. Usar cuando el usuario pide ponerse
  al día («¿qué me perdí?», «revisá mis notificaciones», «resumen de Slack», «¿qué tengo hoy?»), al empezar la
  jornada, o con /sherpa. No responde, no marca nada como leído y no publica: sólo lee y entrega el resumen
  (responder es `herald`). Tampoco diseña ni automatiza esta revisión; si el usuario quiere automatizar su repaso
  diario, es `foundry`.
argument-hint: "[desde cuándo, si no es la jornada anterior]"
---

# Sherpa: el que guía a la cordada y te pone en contexto

El sherpa conoce la montaña y carga lo pesado para que el otro llegue con aire. Esta skill mira todo lo que pasó
desde la última jornada, en todas las fuentes que el usuario conectó, y le entrega **lo que tiene que saber y lo que
le toca hacer**, en una pantalla.

## Las reglas (no se negocian)

1. **Primero la identidad, fuente por fuente.** Antes de leer, verificá que la cuenta de **cada** fuente sea la del
   usuario: que una sea suya no dice nada de las otras. La que no coincide **no se lee** y se avisa arriba de todo:
   leer la cuenta de otra persona expone sus conversaciones privadas. Cómo se verifica y cómo se consigue un conector
   propio es de `quarry` (sus conectores).
2. **Sólo lectura.** No responde, no reacciona, no marca como leído, no archiva. La única escritura es **entregar el
   resumen**, por la autorización permanente acotada de la configuración (`herald`).
3. **Nada se descarta en silencio.** Lo que se clasifica como ruido aparece en una lista plegada al final. Ante la
   duda entre dos categorías, va a la más alta.
4. **Los conteos cierran:** leídos = urgentes + pendientes + contexto + ruido, por fuente y en total. Si no cierran,
   se dice.
5. **Una fuente que falla va arriba de todo.** «No pude leer el correo» es lo primero que se lee, no una nota al pie.

## Las fuentes

`sherpa` no sabe de antemano qué fuentes hay: las declara el usuario en la configuración del ambiente (plantilla en
[referencias/ambiente-ejemplo.md](referencias/ambiente-ejemplo.md)). Cada fuente dice:
- qué es y con qué conector se lee (y de quién es la cuenta, verificada con fecha);
- **qué cuenta como novedad** en ella: una mención, un mensaje directo, un correo sin responder, una reunión, un
  ticket asignado, un PR que espera revisión, un estado que cambió;
- cómo se busca por fecha, y el tope de lectura si lo hay.

Chat, correo y calendario son los ejemplos de la plantilla, no un límite. Si falta la configuración y la sesión es
interactiva, se pide; si es una corrida programada, se entrega un resumen que dice que falta y se termina.

**Un lector por fuente.** Con muchas fuentes, cada una puede leerla un subagente (el pedido sigue `tokenwise`). El
lector **no resume**: devuelve ítems normalizados, y el cruce y la clasificación los hace `sherpa`. Si no, se pierde
lo que sólo se ve al juntar fuentes (un pedido del chat que ya se resolvió por correo).

| Campo del ítem | Qué lleva |
|---|---|
| Fuente | De dónde viene |
| Fecha y hora | Cuándo pasó |
| Quién | Quién lo escribió o lo cambió |
| Tema | Cliente, pedido, proyecto o el identificador que use el ambiente |
| Qué | Una línea |
| ¿Le pide algo al usuario? | Sí o no, y qué |
| Enlace | Para abrirlo |

## El procedimiento

1. **Ventana.** Desde el inicio de la jornada anterior según el horario configurado (o lo que pida el usuario). Se
   dice al principio del resumen: «Desde el viernes 16:00 hasta hoy 9:00».
2. **Identidad** (regla 1), fuente por fuente.
3. **Recolectar** las novedades de cada fuente, con búsquedas filtradas por fecha antes que leyendo todo. Si el
   volumen supera el tope configurado, se prioriza lo más activo y **se dice qué quedó sin leer**.

   **Control positivo.** Antes de concluir «0 novedades» en una fuente, probá la búsqueda con un caso que sabés que
   existe: las plataformas suelen guardar las menciones como un ID (del usuario o del grupo), no como el nombre. Sin
   ese control, el resultado va como «no verificado». Los resúmenes anteriores de la propia `sherpa` no se cuentan.
4. **Una sola línea de tiempo.** Juntá los ítems de todas las fuentes y ordenalos por tema y por hora. Un pedido puede
   quedar resuelto en otra fuente minutos después, y entonces ya no es pendiente. Para dar contexto a un pendiente se
   leen el hilo y lo relacionado en las otras fuentes, hasta el tope de contexto configurado.
5. **Clasificar** cada ítem o grupo:

   | Categoría | Criterio |
   |---|---|
   | **Urgente** | Coincide con una alarma de la configuración (cliente afectado, plazo hoy, algo caído), o lo pide alguien con un plazo vencido |
   | **Pendiente tuyo** | Una pregunta o un pedido dirigido al usuario o a su grupo, sin respuesta de él todavía en ninguna fuente |
   | **Contexto** | No le pide nada, pero cambia algo de su trabajo: una decisión, un precio, un estado, un cliente de su zona. Incluye lo que el usuario preguntó y todavía espera |
   | **Ruido** | Saludos, anuncios generales, conversaciones ajenas a su zona |

   Si el criterio de urgencia del área está escrito en una skill de dominio, se usa esa.
6. **Armar el resumen**, pensado para leerse en el celular:
   1. Ventana, qué fuentes se leyeron y, si las hubo, fallas de lectura.
   2. **Hoy y esta semana**, si alguna fuente trae agenda: reuniones con hora y las invitaciones sin responder.
   3. **Urgente**: una línea por ítem, con quién, qué pide y el enlace.
   4. **Pendientes tuyos**, igual, ordenados por antigüedad.
   5. **Contexto**, agrupado por tema; una o dos líneas por grupo.
   6. **Ruido**: la cuenta y la lista plegada.
   7. Conteos por fuente y en total.

   Si pasa de una pantalla, se recorta el contexto, nunca lo urgente ni los pendientes.
7. **Entregar:** en la sesión, en el chat; en una corrida programada, en el destino de la autorización permanente
   acotada (por ejemplo, un mensaje privado al propio usuario). Nada más se escribe.

## Lo que no hace (todavía)

Buscar lo necesario para resolver cada pendiente y dejar un borrador de respuesta. Cuando se sume, el borrador lo
prepara `sherpa` y el envío pasa por `herald`. Está anotado en el buzón; se suma cuando la versión actual demuestre
que no se le escapa nada.

## Cómo se combina

- Nació en `foundry`; su predicción está en el registro de automatizaciones del ambiente.
- `quarry`: conectores e identidad de cada fuente.
- `tokenwise`: el pedido de lectores cuando hay muchas fuentes.
- `herald`: la entrega por la autorización permanente acotada, y cualquier respuesta.
- Las skills de dominio del ambiente dan el criterio de urgencia y el vocabulario.
- `hallmark` si el resumen lleva cifras que hay que verificar.
