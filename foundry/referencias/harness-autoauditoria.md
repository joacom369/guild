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
python foundry/scripts/auditar_gremio.py --dinamico [--registros DIR] [--trabajo DIR] [--al-buzon]
python foundry/scripts/auditar_gremio.py --autoprueba
python foundry/scripts/auditar_gremio.py --estricto
```

`--autoprueba` siembra un gremio con fallas conocidas y falla si un detector no las ve. `--estricto` sale con 1
cuando hay un error (skill propia sin caso negativo, o sin `evals/piso.json`). Sin esa bandera el script sale 0
aunque haya avisos: el reporte es la salida.

En cada pull request, en cada push a `main` y los lunes a las 09:00 (America/Buenos_Aires), GitHub Actions corre
[`.github/workflows/gremio.yml`](../../.github/workflows/gremio.yml): las dos autopruebas, este script con
`--estricto` y `empaquetar.py`.

[`corregir_gremio.py`](../scripts/corregir_gremio.py) reescribe un enlace roto de la tabla de `AGENTS.md` sólo
cuando hay un único archivo con ese nombre, y sube ese cambio. No edita una skill, no toca una description, no
crea un `piso.json` y no cambia dueños. Esos errores dejan el check en rojo: son el corte. Los avisos (solape,
regla casi igual) no bloquean y no se corrigen para silenciar el auditor. Un push a `main` sólo controla; no
corrige sobre `main`. La rutina semanal, si hay un enlace así, abre un PR. El merge sigue siendo del usuario.

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

## Paso dinámico

El estático mira si los oficios se pisan entre sí. El dinámico mira el trabajo ya hecho y propone qué sumaría
productividad a los subagentes, o un mejor resultado para el usuario. Se corre con `--dinamico`.

Lee sólo los registros que el gremio ya escribe. Dónde viven lo fija `foreman` (`referencias/ambiente-ejemplo.md`):
por defecto `~/.foreman/`.

| Registro | Qué propuesta sale |
|---|---|
| `DELEGACIONES.md` | **Común:** varios encargos sin una comprobación que el agente pueda correr; el mismo pedido repetido; la misma herramienta faltante en más de un oficio. **Puntual:** un oficio cuyos resultados no se usaron, o al que siempre le falta lo mismo. Las columnas que reconoce son las que ya nombra `tokenwise`: pedido, oficio, si se usó, y si están, comprobación y qué faltó |
| `ESTADO.md` (con `--trabajo`) | **Resultado:** un «quedó abierto» que se repite en los tramos. **Puntual:** una lección de método que nombra un oficio. El formato del estado es de `provenance` |
| `AUTOMATIZACIONES.md` | Una predicción con la medición vencida. Compararla es de `foundry` |
| `IDEAS.md` | Una idea descartada no se vuelve a proponer |

`--al-buzon` agrega las propuestas nuevas a `IDEAS.md`, con estado `nueva`. No pisa las descartadas. No edita
ninguna skill.

### Por qué no es un subagente prendido siempre

Un agente que estudie «constantemente» el trabajo de los demás lee sesiones enteras y gasta la cuota aunque no haya
nada nuevo. Mirar ese historial pide permiso antes, diciendo qué se va a leer y cuánto cuesta: es la regla 6 de
`foreman`, y acá no se copia. Los registros de arriba ya son el rastro del trabajo; alcanzan para ver el patrón.

La cadencia la pone una rutina (escalón 7 de `foundry`): en Grok Bot, una `UpdateRoutine`. El script es el escalón
3. Un subagente (escalón 4) entra sólo cuando una propuesta señala una carpeta demasiado grande para esta corrida.
Eso es una ficha de `tokenwise`, la aprueba `foreman`, y lee esa carpeta. No queda un `Task` eterno.

Cada propuesta dice a qué clase pertenece:

- **Común.** El mismo hueco en más de un oficio, o un encargo que se repite. Sube la productividad de los
  subagentes en general.
- **Puntual.** El hueco es de un solo oficio. Mejora la herramienta o el resultado de ese agente para el usuario.
- **Resultado.** Un tramo que queda abierto, o una predicción que ya había que medir.

## Qué queda a mano

- Si un solape de palabras es un robo de momento de verdad. Hace falta cargar las dos skills a la vez.
  `claude plugin eval` no tiene esa opción.
- Si un texto casi igual es una regla copiada o la misma plantilla usada dos veces (por ejemplo, la fila del
  registro del ambiente).
- Si un dueño externo (`ponytail`, y `dataviz` cuando el mapa lo nombre en §3) tiene que entrar al repo.
- El comportamiento de una plataforma. Eso lo prueba el checklist de su adaptador.
- Que ninguna tasa del piso baje. Lo controla `empaquetar.py`.
- Si una propuesta dinámica conviene aplicarla. El script la deja en el buzón; la skill cambia cuando el usuario la
  aprueba.

## El ciclo, cada vuelta

1. **El piso sólo sube.** La regla es de [escribir-skills.md](escribir-skills.md). Este script sólo avisa si falta
   el archivo `evals/piso.json`.
2. **El buzón de `foreman`.** Un hallazgo que pide cambiar una skill no se aplica en el momento: va al buzón, con
   fecha, área y por qué importa. Lo aplica el usuario (regla 5 de `foreman`).
3. **La predicción de `foundry`.** Correr este script antes de cada PR es un script (escalón 3 de la escalera de
   `foundry`). Si se adopta como hábito, la fila va al registro de automatizaciones del ambiente, con una
   predicción fechada: cuántos avisos por corrida resultan ser un solape real y cuántos son ruido. Sin esa
   medición no se sube de escalón. La fila no se escribe en este repositorio.
4. **Antes de empaquetar o de abrir un PR** de oficios: `python foundry/scripts/auditar_gremio.py`. La CI de arriba
   lo corre con `--estricto`. Un error (falta el caso negativo o falta el piso) se mira antes de empaquetar. Los
   avisos se leen; no bloquean solos.
5. **Después de un tramo de trabajo**, `python foundry/scripts/auditar_gremio.py --dinamico --trabajo <proyecto>`.
   Si la rutina está aceptada, `--al-buzon` deja las propuestas nuevas. Aplicarlas sigue siendo del usuario.
6. **La autoprueba** se corre cuando se toca el script, para ver que los detectores siguen disparando. Incluye un
   trabajo sembrado: la propuesta común, la puntual, la descartada que no vuelve, y el buzón que no se duplica.

## Cómo se combina

- `foreman` regla 5: las mejoras se proponen, no se aplican.
- `hallmark` sigue siendo el acta de un entregable con cifras. Este script no es esa acta.
- Los límites para que varios agentes no se pisen en una plataforma son del adaptador de esa plataforma
  (fila en `mapa/MAPA.md` §3). `foreman` y `tokenwise` apuntan; no los copian.
