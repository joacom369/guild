# Harness de autoauditoría del gremio

Dueño: `foundry` (cómo se escribe una skill, y el piso de disparo). El script es
[`../scripts/auditar_gremio.py`](../scripts/auditar_gremio.py). Los demás oficios apuntan acá; no copian el ciclo.

Sirve para ver, antes de empaquetar o de abrir un PR, si dos oficios se pisan. No reemplaza las pruebas de disparo
ni el piso de tasas: eso lo controla `empaquetar.py`. La regla del piso está en
[escribir-skills.md](escribir-skills.md).

## Cómo se corre

Desde la raíz del repositorio, con la biblioteca estándar:

```bash
python foundry/scripts/auditar_gremio.py
python foundry/scripts/auditar_gremio.py --autoprueba
python foundry/scripts/auditar_gremio.py --estricto
```

`--autoprueba` siembra un gremio con fallas conocidas y falla si un detector no las ve. `--estricto` sale con 1
cuando hay un error (skill propia sin caso negativo, o sin `evals/piso.json`). Sin esa bandera el script sale 0
aunque haya avisos: el reporte es la salida.

Los cortes (cuántas palabras, qué ratio, qué tan rara tiene que ser una palabra) están al principio del script.
Un aviso es una pista. Confirmarla sigue a mano.

## Qué mira solo

| Chequeo | Qué cuenta como hallazgo |
|---|---|
| Caso negativo | Una skill propia cuya `description` no dice cuándo no cargarla, o no nombra al otro oficio entre comillas invertidas |
| Robo de momento | Palabras del «Usar…» (y anclas raras del preámbulo) compartidas por dos skills. Si el caso negativo ya nombra a la otra, es info |
| Regla duplicada | Un enunciado casi igual en dos `SKILL.md`, o una ventana de palabras idéntica |
| Piso presente | Una skill propia sin `evals/piso.json`. No mira las tasas |
| Dueños | La tabla de [`mapa/MAPA.md`](../../mapa/MAPA.md) §3: la misma regla en dos filas, o un dueño que no está en el repo ni en la lista de oficios externos |
| Índice | [`AGENTS.md`](../../AGENTS.md): enlace roto, skill propia fuera de la tabla, dos momentos con las mismas palabras |

Las skills de terceros (`impeccable`, `design-taste-frontend`) no entran al piso ni al caso negativo del gremio.
Si una se carga sola, sí entra al solape de momento. `design-taste-frontend` declara que sólo se carga por nombre:
el script lo anota y no la compara.

## Qué queda a mano

- Si un solape de palabras es un robo de momento de verdad. Hace falta cargar las dos skills a la vez.
  `claude plugin eval` no tiene esa opción.
- Si un texto casi igual es una regla copiada o la misma plantilla usada dos veces (por ejemplo, la fila del
  registro del ambiente).
- Si un dueño externo (`ponytail`, y `dataviz` cuando el mapa lo nombre en §3) tiene que entrar al repo.
- El comportamiento de una plataforma. Eso lo prueba el checklist de su adaptador.
- Que ninguna tasa del piso baje. Lo controla `empaquetar.py`.

## El ciclo, cada vuelta

1. **El piso sólo sube.** La regla es de [escribir-skills.md](escribir-skills.md). Este script sólo avisa si falta
   el archivo `evals/piso.json`.
2. **El buzón de `foreman`.** Un hallazgo que pide cambiar una skill no se aplica en el momento: va al buzón, con
   fecha, área y por qué importa. Lo aplica el usuario (regla 5 de `foreman`).
3. **La predicción de `foundry`.** Correr este script antes de cada PR es un script (escalón 3 de la escalera de
   `foundry`). Si se adopta como hábito, la fila va al registro de automatizaciones del ambiente, con una
   predicción fechada: cuántos avisos por corrida resultan ser un solape real y cuántos son ruido. Sin esa
   medición no se sube de escalón. La fila no se escribe en este repositorio.
4. **Antes de empaquetar o de abrir un PR** de oficios: `python foundry/scripts/auditar_gremio.py`. Un error (falta
   el caso negativo o falta el piso) se mira antes de empaquetar. Los avisos se leen; no bloquean solos.
5. **La autoprueba** se corre cuando se toca el script, para ver que los detectores siguen disparando.

## Cómo se combina

- `foreman` regla 5: las mejoras se proponen, no se aplican.
- `hallmark` sigue siendo el acta de un entregable con cifras. Este script no es esa acta.
- Los límites para que varios agentes no se pisen en una plataforma son del adaptador de esa plataforma
  (fila en `mapa/MAPA.md` §3). `foreman` y `tokenwise` apuntan; no los copian.
