# Auditoría independiente: el contrato común

Este archivo es el **dueño del contrato** que cumple cualquier auditor, sea del oficio que sea. Qué busca cada uno
según el trabajo está en el catálogo: [auditores.md](auditores.md).

## Cuándo y quién lo pide

- **Cada jefe pide su auditor.** El oficio que hizo un trabajo sustancial (código, cifras, una página, un modelo,
  una extracción) incluye en su ficha de delegación (`tokenwise`) el auditor especializado en ese trabajo. Se
  aprueba como cualquier delegación: si el costo se paga con lo que evita.
- **En una ronda grande**, además, `hallmark` hace una mirada cruzada final sobre el entregable completo: un informe
  que sostiene una decisión, un modelo nuevo, un tablero que va a usar otro equipo. También cuando el usuario la pide.
- No en cada cambio chico: ahí alcanzan los niveles 1 y 2.

¿Por qué afuera? El que hizo el trabajo tiene el contexto lleno de su propio razonamiento; el auditor llega limpio y
puede cargar con las normas y las listas que el otro ya no ve.

## El encargo

El auditor recibe **el trabajo y las fuentes, no tu plan ni tus conclusiones**. Si le contás qué esperás encontrar,
te lo confirma.

1. **Objetivo:** «Encontrá errores en <esto> antes de que llegue a <lector>, que lo va a usar para <decisión>».
2. **Qué leer:**
   - el trabajo final (el entregable, el diff, la corrida);
   - **el pedido original**, con sus criterios de aceptación, tal como lo hizo el usuario;
   - las fuentes: salidas, consulta, ficha de datos, las normas del repositorio.

   Nada más.
3. **Qué buscar, en dos ejes que no se mezclan:**
   - **Eje del pedido:** ¿hace lo que se pidió? Qué faltó, qué sobró, qué está hecho distinto de lo pedido. Cada
     hallazgo cita el pasaje del pedido.
   - **Eje del oficio:** la lista de control de su tipo de trabajo, del catálogo.
4. **Qué no hacer:** no editar archivos, no rehacer el trabajo, no opinar sobre estilo salvo que cambie lo que se
   entiende o lo que hace.
5. **Formato de devolución:**
   - hasta 10 hallazgos por eje, en **listas separadas**; no se fusionan ni se reordenan entre ejes;
   - cada uno con ubicación, qué está mal, la evidencia (archivo y línea, o fila de la fuente) y la gravedad:
     *rompe* / *cambia la conclusión* / *cambia una cifra* / *confunde al lector*;
   - cada uno rotulado como **violación** (contra una regla o el pedido escritos) o **juicio** (opinión fundada del
     auditor);
   - si no encuentra nada grave, lo dice en una línea; no hace falta llenar la lista.
6. **Un control que pueda correr**, con la **ruta absoluta** y los argumentos: `cifras.py` para cifras, las pruebas
   del proyecto para código, `foto_pagina.py` para una página. El auditor no carga la skill: sin la ruta no lo
   encuentra.

Describí el trabajo, no un personaje: «revisá como un auditor que busca ingresos sin respaldo», no «sos un auditor».

## Lo que devuelve

Cada hallazgo se verifica antes de aceptarlo:

| Resultado | Qué se hace |
|---|---|
| Confirmado | Se corrige en el proceso y se vuelve a correr el nivel 1 |
| Refutado | Se anota por qué (con la evidencia), no se descarta en silencio |
| No se puede decidir | Va al acta como abierto y se le muestra al usuario |

Si el auditor y tu diagnóstico discrepan y los dos tienen evidencia, se reportan los dos. No se elige el cómodo.
