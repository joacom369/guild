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
- **El piso de disparo sólo sube.** Cada skill guarda en `evals/piso.json` los casos que pasan, el modelo y la huella
  de la description probada. `empaquetar.py` no empaqueta si la description cambió sin volver a probarse, si falta un
  caso del piso o si uno falla en su corrida más nueva. Con todo en verde, `python empaquetar.py --piso <skill>` lo
  sube; bajarlo (borrar o cambiar un caso) se hace a mano, con el motivo en el mapa. Así una mejora no le roba en
  silencio el momento a otra skill.

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

---

Adaptado de la skill `writing-for-agents` de Matt Pocock (github.com/mattpocock/skills, licencia MIT), con
palabras propias.
