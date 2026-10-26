# Revisión independiente: el detalle

## Cuándo

- Rondas grandes: un informe que sostiene una decisión, un modelo nuevo, un tablero que va a usar otro equipo.
- Cuando el usuario la pide.
- No en cada cambio: una por ronda grande. Lanzarla cuesta tokens y tiempo: se pide con la ficha de delegación de
  `tokenwise`.

## El encargo

El revisor recibe **el entregable y las fuentes, no tu plan ni tus conclusiones**. Si le contás qué esperás encontrar,
te lo confirma.

1. **Objetivo:** «Encontrá errores en este entregable antes de que llegue a <lector>, que lo va a usar para <decisión>».
2. **Qué leer:** el entregable final y las rutas de las salidas, la consulta y la ficha de datos. Nada más.
3. **Qué buscar**, en concreto:
   - cifras que no salen de las salidas o que no coinciden con ellas;
   - conclusiones más fuertes de lo que permiten los datos (causalidad sin diseño, «siempre» sin probar todos los casos);
   - supuestos presentados como datos, y escenarios presentados como pronósticos;
   - identidades que no cierran, unidades o períodos mezclados;
   - lo que el lector va a entender mal (un gráfico sin eje, una escala engañosa, un vacío leído como cero);
   - lo que falta para que la conclusión se sostenga.
4. **Qué no hacer:** no editar archivos, no rehacer el análisis, no opinar sobre estilo salvo que cambie lo que se
   entiende.
5. **Formato de devolución:** una lista priorizada de hasta 10 hallazgos. Cada uno con ubicación, qué está mal, la
   evidencia (archivo y fila de la fuente) y la gravedad: *cambia la conclusión* / *cambia una cifra* / *confunde al
   lector*. Si no encuentra nada grave, que lo diga; no hace falta llenar la lista.
6. **Un control que pueda correr:** el comando de `cifras.py` completo, con la **ruta absoluta** del script (la
   carpeta `scripts/` de esta skill) y los mismos argumentos. El revisor no carga la skill: sin la ruta no lo
   encuentra.

Describí el trabajo, no un personaje: «revisá como un auditor que busca ingresos sin respaldo», no «sos un auditor».

## Lo que devuelve

Cada hallazgo se verifica antes de aceptarlo:

| Resultado | Qué se hace |
|---|---|
| Confirmado | Se corrige en el proceso y se vuelve a correr el nivel 1 |
| Refutado | Se anota por qué (con la evidencia), no se descarta en silencio |
| No se puede decidir | Va al acta como abierto y se le muestra al usuario |

Si el revisor y tu diagnóstico discrepan y los dos tienen evidencia, se reportan los dos. No se elige el cómodo.
