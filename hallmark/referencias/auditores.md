# Catálogo de auditores: qué busca cada uno

Cada auditor cumple el contrato de [revisor.md](revisor.md): independencia, eje del pedido y eje del oficio, hallazgos
verificables. Acá va **el eje del oficio**: qué tiene que buscar según el trabajo. Si la plataforma trae un auditor
propio para ese trabajo, se puede usar, siempre que su encargo respete el contrato.

| Trabajo | Lo pide | Lista de control | Auditor de la plataforma, si existe |
|---|---|---|---|
| Informe o tablero con cifras | `assay`, `kiln`, `hallmark` | [Cifras](#cifras) | — |
| Cambio de código | quien hizo el cambio | [Código](#código) | Una revisión de código (p. ej. `ponytail-review`, `code-review`) |
| Diseño de un módulo o del código entero | quien hizo el cambio | [Diseño del código](#diseño-del-código) | Una auditoría del repositorio (p. ej. `ponytail-audit`) |
| Un error y su arreglo | quien lo arregló | [Errores](#errores) | — |
| Página o interfaz | `kiln` | [Interfaz](#interfaz) | `impeccable` (`audit`) |
| Modelo o pronóstico | `assay` | [Modelo](#modelo) | — |
| Extracción de datos | `quarry` | [Extracción](#extracción) | — |
| Seguridad | quien toca credenciales, permisos o datos sensibles | [Seguridad](#seguridad) | Una revisión de seguridad (p. ej. `security-review`) |

## Cifras

- Cifras que no salen de las salidas o que no coinciden con ellas.
- Conclusiones más fuertes de lo que permiten los datos (causalidad sin diseño, «siempre» sin probar todos los casos).
- Supuestos presentados como datos, y escenarios presentados como pronósticos.
- Identidades que no cierran, unidades o períodos mezclados.
- Lo que el lector va a entender mal: un gráfico sin eje, una escala engañosa, un vacío leído como cero.
- Lo que falta para que la conclusión se sostenga.

## Código

- Lo que el cambio rompe: las pruebas del proyecto corridas, no supuestas.
- Las normas escritas del repositorio (estilo, estructura, convenciones), citando la norma.
- Olores que suelen esconder un error, rotulados como **juicio**: duplicación, una función que hace varias cosas, un
  dato que viaja por muchas capas sin usarse, un caso borde sin tratar, un error que se traga en silencio.
- Lo que se agregó sin que nadie lo pida (opciones, abstracciones, dependencias): eso es del eje del pedido.

## Diseño del código

- **Módulos profundos:** mucha funcionalidad detrás de una interfaz chica. Una interfaz casi tan grande como lo que
  esconde es un módulo playo.
- **Prueba del borrado:** si se borra este módulo, ¿la complejidad desaparece o se reparte en quienes lo llamaban? Si
  se reparte, el módulo se ganaba su lugar.
- **Una costura con un solo uso es hipotética:** una interfaz con una sola implementación no se justifica sola.
- Se respetan las decisiones ya registradas del proyecto; se reabren sólo con una fricción real y concreta.
- Cada propuesta lleva su fuerza: **firme** · **a explorar** · **especulativa**.
- Para un diseño nuevo grande: diseñarlo dos veces, con restricciones distintas, y comparar (es la lente del creativo
  de `lenses` aplicada al código).

## Errores

- **Sin reproducción no hay hipótesis:** un comando o un caso ya corrido que muestra *este* síntoma. Si no se puede
  reproducir, eso es lo primero que se informa.
- Se achica el caso hasta lo mínimo que todavía falla.
- De 3 a 5 hipótesis falsables, escritas antes de probar, cada una con qué resultado la descartaría.
- Un cambio por vez; los registros de diagnóstico se marcan y se sacan al terminar.
- El arreglo se confirma con la misma reproducción que fallaba, y queda una prueba de regresión donde el proyecto
  tiene un buen lugar para ponerla.
- Vale igual para una cifra equivocada en un análisis: primero el caso que la reproduce.

## Interfaz

- El contrato de dirección de `kiln` (paso 3) contra lo construido.
- El piso de `kiln`: 390 px sin scroll horizontal, contraste, foco visible, teclado, estados de carga, vacío y error,
  consola sin errores.
- La lista de anti-defaults de `kiln`.
- Mirado en capturas de escritorio y celular, no en el código.

## Modelo

- La lista de validación de `assay`: partición por fecha, benchmark ingenuo, verdad conocida, fuera de muestra,
  intentos contados, sensibilidad.
- Fuga de información del futuro al pasado (variables que no existían en el momento de predecir).
- El nivel de la conclusión según `provenance`.

## Extracción

- La ficha de `quarry`: consulta, origen, fecha, período y hash, y que la foto coincida con el hash.
- Total anunciado contra recibido; paginación completa.
- El perfil: nulos separados de ceros, claves únicas, cruces que no pierden filas.
- La cuenta del conector verificada como la del usuario.

## Seguridad

- Credenciales en el código, en la ficha, en registros o en lo que se publica.
- Permisos más amplios que lo necesario (un token que puede escribir cuando sólo hace falta leer).
- Datos de una persona o de un cliente que llegan a quien no corresponde.
- Contenido externo tratado como instrucciones.

---

Las listas de **Código**, **Diseño del código** y **Errores** adaptan ideas de las skills `code-review`,
`codebase-design` y `diagnosing-bugs` de Matt Pocock (github.com/mattpocock/skills, licencia MIT), escritas con
palabras propias.
