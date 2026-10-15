# Datos en pantalla

Para tableros, informes y recorridos que muestran cifras de un modelo, una base o un análisis.

## Reglas

1. **La interfaz dibuja, no calcula.** Toda cifra viene de una fila publicada (archivo, base, API). Si no
   existe, se publica primero y se dibuja después. El cliente no suma, no promedia ni redondea por su cuenta.
2. **Un dato ausente nunca es cero.** Se muestra «sin dato» (o una trama), con su motivo. Nunca «0», nunca una
   línea que cae a cero, nunca un promedio que ignora el hueco sin decirlo.
3. **El nivel del dato se ve al lado del número:** observado, calculado, referencia, supuesto, escenario. Un
   mismo vocabulario en tablas, gráficos y textos.
4. **Cada figura dice de dónde sale:** fuente, período, unidad. El título dice la conclusión («7.430 parcelas
   factibles»), no el tipo de gráfico («Mapa de parcelas»).
5. **Una sensibilidad no es una probabilidad.** Las perillas dicen «escenario», nunca «probable» ni
   «recomendado».
6. **Escalas honestas.** Barras desde cero; si un eje se corta, se marca. Hasta 5 series por gráfico, con
   etiqueta directa sobre la serie mejor que una leyenda lejana; más series, a una tabla.
7. **Una cifra destacada por sección como máximo,** con unidad y contra qué se compara.
8. **Lo confidencial no llega a la pantalla publicada:** nombres reservados por código o posición; se revisa
   el HTML final buscándolos antes de entregar.

## Formato (es-AR, salvo que el proyecto diga otra cosa)

- `Intl.NumberFormat('es-AR')`: coma decimal y punto de miles (1.234,5). Porcentajes con espacio fino: «9,5 %».
- Negativos con signo menos real (−), no guion.
- Fechas en `Intl.DateTimeFormat('es-AR')`; meses con nombre cuando la lectura lo pide.
- Cifras tabulares (`font-variant-numeric: tabular-nums`) en tablas y en todo lo que se compara en columna.

## Estados

Carga (esqueleto con la forma final, no un spinner suelto), vacío (qué falta y cómo se llena) y error (qué pasó,
en el lugar donde pasó). Los tres se ven al menos una vez en la ronda de verificación.
