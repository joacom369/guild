# Registro, aprendizaje y comunicación: el detalle

## Registro de decisiones
- Cada decisión material: Antes / Ahora / Por qué, quién la tomó (usuario o análisis) y fecha.
- Si una cifra publicada cambia: cuál era, cuál es y qué la movió.
- Una auditoría produce una lista de mejoras trazable (pendiente / hecha), no cambios sueltos.

## Aprender de los errores
- Clasificar cada error: (a) dirección, (b) magnitud, (c) medida contaminada o diseño mal especificado, (d) supuesto que cayó, (e) quiebre reflexivo (el objeto reaccionó).
- Destilar una regla sólo de los tipos que enseñan método (b, c, e) y sólo si es sobre el método, no sobre el caso.
- Consultar las lecciones antes de fijar una magnitud y declarar cuáles se tuvieron en cuenta.
- Cada ejercicio difícil cierra con «dónde crujió el método» y con lo que funcionó, para no tocarlo.
- Separar tres piezas: instrucciones estáticas, memoria que crece (lecciones, predicciones, decisiones) y la herramienta que consulta. El prompt no aprende; el registro sí.
- Formatos simples y legibles a ojo (texto, JSON plano, versionados); la complejidad llega cuando el volumen la justifica.

## Comunicar
- Antes de escribir: para quién, por qué le importa y qué tiene que poder hacer con lo que lee (actuar, aclarar, actualizarse, prestar atención). La estructura sirve a esa acción.
- Lo más importante primero; el detalle después.
- Cada número con su unidad, su base y su nivel (preliminar o definitivo).
- Lo que no se sabe va a la vista, no al pie.
- Un entregable declara: fuente, cobertura, período, fecha de verificación, límites, cita del productor y lo que NO hace.
- Una guía de lectura por archivo de salida: qué columnas mirar y qué hacer según el valor.
- Declarar las dependencias externas (qué deja de funcionar sin conexión).
- Respetar la extensión: la síntesis forzada es parte del método.

## Un informe que no se cae
Rúbrica mínima: título con palabras clave; introducción con objetivo, hipótesis
y método; apartado metodológico; resultados ordenados con un criterio;
conclusión que vuelve al objetivo, la hipótesis y el método; referencias.
Errores típicos: sin hipótesis, sin fuentes, variables sin definir, saltos
temporales sin explicar, gráficos sin ejes, resultados sin orden, conclusión
que no proyecta.

- Hipótesis que se cierran como confirmadas, refutadas o matizadas, con sus
  supuestos más sensibles y la información que faltó.
- Ante un concepto ambiguo, declarar el criterio adoptado antes de calcular.
- Mostrar el desarrollo, no sólo el resultado.
- Si dos personas resolvieron distinto, anexar las dos resoluciones en lugar de
  elegir una en silencio.
- Atribuir una posición a un autor con sus textos y citas, no con la etiqueta
  de su escuela; un diagnóstico compartido no obliga a compartir la propuesta.
- Presentar un marco diciendo de dónde viene y quién lo critica; reconstruir el
  pasado sin anacronismo.
- Entrenar la revisión con frases plausibles pero falsas («Comente»): ¿qué le
  falta o qué supone?

## Plantilla: archivo de estado (bitácora)

Un proyecto de más de una sesión lleva un archivo de estado en su raíz (por
ejemplo `ESTADO.md`). **Se lee al retomar**, antes de tocar nada; cuándo se
escribe lo dice `foreman` (una línea por tramo y un orden al cerrar). Corto: si
pasa de una pantalla, lo viejo se archiva.

```markdown
# Estado · <proyecto> · actualizado <fecha>

## Dónde estamos
Una o dos líneas: qué está hecho, qué está a medias, qué sigue.

## Decisiones
| Fecha | Qué | Antes | Ahora | Por qué | Quién |
|---|---|---|---|---|---|

## Cifras publicadas que cambiaron
| Cifra | Era | Es | Qué la movió |
|---|---|---|---|

## Tramos
- <fecha> · qué salió · cifras con su rótulo (observado, calculado…) · qué quedó abierto

## Pendientes
- [ ] … (quién, para cuándo, qué lo destraba)

## Lecciones de método
- … (tipo de error b, c o e; sólo si es sobre el método, no sobre el caso)
```

## Plantilla: una entrega

Para la respuesta o el informe que cierra un trabajo. Se ajusta la extensión al
lector; el orden no.

```markdown
**Conclusión** (nivel: preliminar sobre referencias / definitivo / techo)
Una o dos frases. Si no se puede concluir: «no concluyo» y qué haría falta.

**Opciones** — cada una con su consecuencia y lo que exige. La decisión es del usuario.
| Opción | Qué pasa | Qué exige | Riesgo principal |
|---|---|---|---|

**Lo que no se sabe** — y qué lo resolvería (dato, cotización, prueba).

**Cifras clave** — cada una con unidad, período y naturaleza
(observado · calculado · reconstruido · supuesto · escenario · pendiente).

**Límites** — qué no hace este trabajo y qué controles no se corrieron (acta de `hallmark`).
```
