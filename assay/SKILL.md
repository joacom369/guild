---
name: assay
description: Procedimiento para analizar o modelar datos ya extraídos y dejar salidas reproducibles. Escribe el plan antes de ver resultados (pregunta, técnica, métrica, benchmark ingenuo, qué cambiaría la conclusión), hace el pre-análisis, calcula siempre con código que corre en una carpeta nueva con su ficha (entradas verificadas, semilla, versión), cuenta todos los intentos, aplica el protocolo de modelado (partición por fecha, diagnóstico) y la sensibilidad, y entrega la carpeta de salidas a la fase siguiente. Usar al calcular indicadores, estimar un modelo, hacer un pronóstico o una evaluación, comparar grupos o escenarios, o con /assay. No elige la técnica (`compass`), no saca los datos (`quarry`) ni controla el entregable final (`hallmark`); el criterio sobre cada cifra es de `provenance`.
argument-hint: "[qué se analiza]"
---

# Assay: el ensayo de la muestra

Entre la cantera y el horno está el laboratorio: la muestra se ensaya para saber qué tiene y cuánto, con un método
que otro puede repetir y obtener lo mismo. Esta skill es ese procedimiento. Los axiomas (qué es cada cifra, con qué
nivel se concluye, cómo se valida) son de `provenance`; acá van **los pasos**.

## Las reglas (no se negocian)

1. **Ninguna cifra se calcula en la conversación.** Todo número sale de código guardado en un archivo y corrido
   sobre la foto de datos. Una cuenta «de cabeza» es un supuesto, y se rotula así.
2. **El plan va antes que los resultados.** Lo que se cambia después de ver un resultado se anota (antes, ahora, por
   qué) y cuenta como un intento más.
3. **Todos los intentos cuentan.** Cada corrida queda en su carpeta; no se borran las que no gustaron. Si se probaron
   veinte especificaciones, se dice que fueron veinte.
4. **Un resultado malo se informa tal cual.** Si nada le gana al benchmark ingenuo, esa es la conclusión.
5. **Las corridas no se pisan** y no se corre sobre datos que cambiaron desde su ficha.

## El procedimiento

### 1. Partir de lo verificado

- La técnica viene del veredicto de `compass`; si no hay veredicto y la técnica no es obvia, se pide.
- Los datos son una foto con ficha (de `quarry`). Si vienen de otro lado, se les hace la ficha antes de empezar, incluidos los que el orquestador verificó directo en la sesión.

### 2. Escribir el plan (`PLAN.md` en el proyecto)

```markdown
# Plan · <análisis> · <fecha>
- Pregunta: <la pregunta de análisis, no la práctica>
- Unidad de análisis y período: …
- Técnica y su supuesto clave: … (veredicto de compass)
- Métrica de éxito y benchmark ingenuo: …
- Qué resultado cambiaría la conclusión (umbral): …
- Qué NO se va a concluir con esto: …
- Datos: <carpeta de la foto> (ficha del <fecha>)
```

### 3. Pre-análisis, antes de los resultados

Unidad de análisis, distribuciones, valores extremos (qué son, si son errores o casos reales y qué se hace con ellos y
por qué), composición de los grupos, faltantes (el perfil de `quarry` es el punto de partida) y fuentes de sesgo
posibles. Se le muestra al usuario **antes** de los resultados: si cambia el plan, se cambia ahora.

### 4. Calcular con una corrida

El análisis es un script que lee la foto y escribe sus salidas en la carpeta que le da `corrida.py`:

```bash
python scripts/corrida.py --nombre ventas-por-region --entrada datos/2026-10-25_ventas -- python analisis.py
python scripts/corrida.py --verificar salidas/2026-10-25_101500_ventas-por-region
```

`corrida.py` verifica que la entrada coincida con su `FICHA.json` (si no coincide, no corre). Después crea
`salidas/<fecha>_<hora>_<nombre>/` y le pasa al script `CORRIDA_DIR` y `CORRIDA_SEMILLA`. Al terminar deja
`CORRIDA.json` con el comando, la semilla, la versión de Python, el commit del repositorio, las entradas verificadas
y el hash de cada salida, y `log.txt` con la salida del script. Las salidas son archivos (CSV, JSON), no texto
impreso: de ahí las va a buscar `hallmark`.

Si el entregable es en LaTeX, el mismo script puede generar un archivo de macros (`cifras.tex`, una macro por cifra calculada) e incluirlo con `\input`: así ninguna cifra calculada se tipea a mano y cada recálculo actualiza todo el informe.

### 5. Si hay un modelo

1. **Partición:** entrenamiento y prueba; con tiempo, por fecha y nunca al azar. El benchmark ingenuo se fija con el
   entrenamiento.
2. **Entrenamiento** sólo con el conjunto de entrenamiento. Cada especificación probada es un intento.
3. **Diagnóstico:**
   - sobreajuste: la métrica en entrenamiento contra la de prueba;
   - supuestos del método y su prueba;
   - estabilidad: otra semilla, otro período;
   - calibración, si el modelo da probabilidades.
4. **Verdad conocida** si el método es nuevo para el caso: datos simulados con el efecto sembrado tienen que
   recuperarlo, y sin efecto sembrado no debe aparecer.

### 6. Sensibilidad

¿Qué variable decide el resultado? Un barrido o un tornado sobre los supuestos. Cuando falta un dato, se calcula el
umbral: el valor al que la conclusión cambia. Cada escenario se rotula como escenario.

### 7. Entregar a la fase siguiente

Una tabla corta para el usuario y para `kiln` y `hallmark`:

| Qué | Valor |
|---|---|
| Corrida que se usa | `salidas/<carpeta>` (y por qué esa) |
| Intentos | N corridas; las descartadas y su motivo |
| Resultado | Qué dice, con su incertidumbre y su nivel (preliminar / definitivo / techo) |
| Contra el benchmark | Cuánto le gana, o que no le gana |
| Para qué sirve y para qué no | … |

## Scripts

`corrida.py` usa sólo la biblioteca estándar de Python. Corre cualquier comando (Python, R, SQL por línea de
comandos), no sólo Python. Ayuda: `python scripts/corrida.py -h`.

## Cómo se combina

- Antes: `compass` (con qué técnica) y `quarry` (la foto con ficha).
- Durante: `provenance` (naturaleza de cada cifra, nivel de la conclusión, hábitos).
- Después: `kiln` o `dataviz` construyen con las salidas; `hallmark` busca cada cifra del entregable en la carpeta
  de la corrida.
- Si hay muchas corridas independientes, `tokenwise` decide si se reparten.
