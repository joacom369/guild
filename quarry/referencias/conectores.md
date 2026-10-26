# Conectores: la cuenta del usuario, con el permiso mínimo

Cualquier oficio que lee una fuente personal del usuario (chat, correo, calendario, repositorios, un CRM) lo hace a
través de un conector. Esta referencia, de `quarry`, dice cómo comprobar que cada uno es suyo y qué hacer cuando no
lo es. La usan `quarry` en sus extracciones y `sherpa` en su lectura diaria. Los comandos de cada plataforma están en
los adaptadores del repositorio de skills (`adaptadores/`).

## Por qué hace falta

En una cuenta compartida (un equipo, una cuenta de la empresa), los conectores de la plataforma pueden estar
autenticados como **otra persona**. Que uno sea del usuario no dice nada de los otros: cada fuente se verifica por
separado.

## Verificar, fuente por fuente

| Fuente | Cómo se verifica sin leer contenido |
|---|---|
| Chat | El perfil de la cuenta conectada (nombre, usuario, correo) |
| Correo | La dirección de la cuenta, o el remitente de un enviado pedido **sólo con metadatos** (sin asunto ni texto) |
| Calendario | El identificador del calendario principal |
| Cualquier otra (repositorio, CRM, tickets) | La herramienta de «quién soy» o el perfil de la cuenta, si la tiene; si no, un dato propio del usuario pedido sólo con metadatos |

Si no coincide, no se lee nada más de esa fuente y se avisa arriba de todo.

## Conseguir un conector propio

En orden, del más simple al más trabajoso:

1. **El conector de la plataforma, autorizado por el usuario.** Si la plataforma permite una autorización por máquina
   o por usuario (OAuth), se usa esa y se verifica.
2. **Un servidor local de sólo lectura con una credencial propia.** Cuando el servicio no deja registrarse solo o
   exige un programa especial, se crea una credencial OAuth propia (por ejemplo, un proyecto en la consola del
   proveedor con su pantalla de consentimiento interna) y un servidor chico que pide **sólo permisos de lectura**.
   Así, aunque algo falle, el token no puede mandar, borrar ni modificar nada. Hay un ejemplo en
   `adaptadores/ejemplos/mcp-lectura-google/` del repositorio de skills.
3. **Sin conector.** La fuente queda fuera y el resumen lo dice arriba.

## Reglas para cualquier conector

- **Permiso mínimo:** sólo lectura, salvo el único destino de entrega que el usuario autorizó.
- **Los secretos no van al chat ni al repositorio:** la credencial y el token viven en la máquina, fuera del control
  de versiones.
- **Lo que «conectado» no prueba:** algunos servidores responden la lista de herramientas sin identificar a nadie.
  Lo que prueba la conexión es una lectura real con la cuenta verificada.
- **Se anota en la configuración del ambiente:** qué conector se usa para cada fuente, de quién es y cuándo se
  verificó.
