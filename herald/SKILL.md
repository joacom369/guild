---
name: herald
description: >
  Procedimiento para escribir fuera de la sesión con permiso: mandar o responder un mensaje o un correo, publicar,
  comentar, cambiar un estado o un registro en un sistema, y también borrar, archivar o pisar algo del usuario. Arma
  la vista previa exacta, pide la aprobación de esa acción puntual, la ejecuta, deja registro y dice cómo se deshace.
  Usar siempre antes de una escritura externa o de borrar algo, cuando el usuario dice «mandale», «respondé»,
  «publicá», «cambiá el estado», «borrá», o con /herald. No redacta el contenido de un análisis o una página (`kiln`)
  ni decide si conviene la acción; tampoco sirve para leer (`quarry`, `sherpa`).
license: MIT
---

# Herald: el heraldo

El heraldo lleva un mensaje en nombre de otro: lo muestra antes, lleva el sello de quien lo autorizó y deja
constancia de que lo entregó. Esta skill es la **única dueña** de cómo se escribe afuera. Los demás oficios, cuando
necesitan escribir, la llaman.

## Las reglas (no se negocian)

1. **Permiso por acción, no general.** «Podés responder a los clientes» no autoriza nada: cada mensaje, cambio o
   borrado se aprueba por separado, viendo exactamente qué sale. La única excepción es una **autorización permanente
   acotada** que el usuario dejó escrita en la configuración del ambiente (por ejemplo, «el resumen diario, a mi
   mensaje privado»): un destino, un tipo de contenido, una fecha de autorización.
2. **Las reglas del ambiente mandan.** Si un guardarraíl prohíbe algo (datos que no salen, precios que no se
   prometen), no se ofrece ni en borrador.
3. **Un agente no escribe afuera por su cuenta.** Un subagente puede preparar el borrador; la ejecución pasa por esta
   skill, con la aprobación del usuario.
4. **Lo que no se puede deshacer se dice antes.** Si la acción es irreversible (un correo enviado, un borrado sin
   papelera), la vista previa lo dice en la primera línea.

## El procedimiento

1. **Preparar.** El contenido lo trae quien lo necesita (una respuesta, un estado, un comentario). Se verifica la
   identidad de la cuenta con la que se va a escribir: tiene que ser la del usuario.
2. **Vista previa exacta.** Lo que se va a ejecutar, tal cual:
   - dónde (sistema, canal, hilo, registro) y como quién;
   - a quién llega, si es un mensaje;
   - el texto completo, o el antes y el después de un cambio;
   - si se puede deshacer y cómo.
3. **Aprobación explícita** de esa acción. Sin respuesta, no se ejecuta. Si el usuario cambia algo, vuelve al paso 2.
4. **Ejecutar** una sola vez, sin reintentos ciegos: si falla, se informa el error y se pregunta.
5. **Registrar** en el registro de escrituras que fija la configuración del ambiente:

   ```markdown
   | Fecha y hora | Dónde | Qué (una línea) | Enlace | Autorizó | Cómo se deshace |
   |---|---|---|---|---|---|
   ```

6. **Confirmar** al usuario con el enlace a lo que se escribió.

## Borrar, archivar o pisar

Mismo procedimiento, con dos agregados en la vista previa: **qué se pierde** (contenido, historial, vínculos) y
**dónde queda una copia**, si la hay. Antes de pisar un archivo o un registro, se mira el contenido actual.

## Cómo se combina

- `foreman` frena antes de toda escritura externa y la deriva acá.
- `sherpa` entrega su resumen por la autorización permanente acotada de la configuración; responder un pendiente es
  una escritura nueva y pasa por acá.
- `foundry`: una automatización que escribe afuera usa este procedimiento o una autorización permanente acotada.
- Las skills de dominio del ambiente dicen qué no puede salir nunca.
