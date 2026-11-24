# Escribir para agentes: skills, índices y archivos de reglas

Vale para todo lo que lee un agente: un `SKILL.md`, sus referencias, `AGENTS.md`, el archivo de reglas del
ambiente. `foundry` lo usa al construir una skill; cualquiera lo usa al editar una.

## El puntero decide cuándo se carga

La `description` de una skill (o la línea de un índice que nombra un archivo) es un **puntero**: dice qué es el
material y en qué casos se busca. De eso depende que se cargue a tiempo.

- **La palabra que dispara, primero.** Lo que el usuario diría va al principio, no al final.
- **Un disparador por rama.** Una rama es un caso que el documento resuelve distinto. Cinco sinónimos del mismo caso
  son una rama escrita cinco veces: se dejan las ramas de verdad.
- **El caso negativo, nombrando al dueño:** «No elige la técnica (`compass`)». Es lo que evita que una skill le robe
  el momento a otra.
- **Sin «: » suelto en el YAML** (rompe la lectura): usar el estilo `>` o comillas. Lo controla `empaquetar.py`.
- Si cambia una description, se corren sus pruebas de disparo.
- **El piso de disparo sólo sube.** Las pruebas de disparo son aleatorias: el mismo caso puede pasar 5 de 5 y después
  1 de 3. Por eso cada skill guarda en `evals/piso.json` una **tasa por caso** medida con 3 corridas o más, además de
  la huella de la description y de cada caso. `empaquetar.py` no empaqueta si la description o un caso cambiaron
  desde que se midieron, si falta un caso o si la corrida más nueva de un caso (con 3 o más) queda más de un fallo
  por debajo de su tasa; una corrida de 1 o 2 sólo avisa. `python empaquetar.py --piso <skill>` mide con las corridas
  posteriores al último cambio del `SKILL.md` y nunca baja una tasa; borrar un caso se hace a mano, con el motivo en
  el mapa. Un caso flojo conocido se deja en el piso con su tasa real (aunque sea 0%): así queda a la vista y sólo
  puede subir.
- **No ajustar la description a la letra del caso.** Si la description copia la frase de la prueba, la prueba pasa
  y no dice nada. Se agrega un caso con otra redacción para ver si el disparo generaliza.
- **Antes de empaquetar o de un PR**, el auditor estático del gremio. Qué mira y el ciclo de mejora están en
  [harness-autoauditoria.md](harness-autoauditoria.md). El piso de tasas sigue siendo de esta página y de
  `empaquetar.py`.

## Arriba lo que se hace, abajo lo que se consulta

- **Pasos** (lo que el agente hace, en orden) en el `SKILL.md`. **Referencia** (reglas, tablas, detalle) en
  `referencias/`, con un enlace que dice cuándo leerla.
- Bajar demasiado esconde lo que el agente necesita; bajar poco infla el archivo y la atención se diluye. Cada skill
  debería leerse entera en un par de minutos.
- Lo que va junto se escribe junto: la definición, la regla y sus excepciones bajo el mismo título.

## Cada paso termina en algo que se puede comprobar

Un paso termina con una condición clara de «hecho»: «cada cifra del entregable encontrada en las salidas», no
«revisar las cifras». Una condición vaga invita a terminar antes de tiempo; una exigente obliga a hacer el trabajo
entero.

## Pedir lo que sí, no prohibir

Escribir una prohibición pone la conducta prohibida en el contexto. Mejor la conducta buscada: «cada cifra con su
fuente» en lugar de «no inventes cifras». Una prohibición queda sólo cuando no hay forma positiva de decirlo (las
reglas «no se negocian» de cada skill), y entonces va con su motivo.

## Palabras que cargan una idea

Una palabra que el modelo ya conoce puede reemplazar una frase repetida: *acta*, *ficha*, *foto*, *corte*, *lente*.
Se repite como palabra, no como explicación, y ancla la misma conducta cada vez que aparece.

## Podar

- **Un dueño por regla:** cada significado en un solo lugar; los demás apuntan. Una copia se desvía (pasó con la
  tabla del ciclo en el mapa).
- **El entorno también es fuente:** no copies lo que ya dicen un script, una configuración o la ayuda de un comando.
- **Cada línea cambia la conducta.** Si el modelo ya lo haría sin que se lo digan, la línea gasta sin aportar: se
  saca.
- **Sedimento:** al editar, sacá lo que quedó viejo, no sólo agregues.
- **Un comportamiento nuevo, ¿pide una skill nueva?** Si se arma combinando lo que ya existe, no: se escribe en la
  skill dueña.

## Seguridad antes de sumar una skill de terceros

Antes de instalar, copiar o versionar cualquier skill ajena:

1. **Licencia explícita y compatible:** comprobar el archivo `LICENSE` del origen; sin licencia abierta explícita (o con términos *source-available* / restrictivos) queda sólo como referencia externa, nunca copiada.
2. **Lectura completa:** revisar `SKILL.md`, `referencias/` y scripts buscando instrucciones ocultas (*prompt injection*), exfiltración de datos/tokens, comandos destructivos o telemetría activa por defecto.
3. **Mínimo privilegio:** auditar `allowed-tools`, hooks de arranque/edición y binarios o descargas que dispare al ejecutarse.
4. **Cuidar el disparo del gremio:** correr `auditar_gremio.py` para ver solapes de `description`; si la skill se invoca sólo por nombre, verificar o evaluar `disable-model-invocation: true`.
5. **Consentimiento:** proponer al usuario qué agrega, licencia y costo/riesgo antes de instalarla o habilitar sus hooks.

---

Adaptado de la skill `writing-for-agents` de Matt Pocock (github.com/mattpocock/skills, licencia MIT), con
palabras propias.
