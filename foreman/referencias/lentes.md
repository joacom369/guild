# Las lentes: contratos

`foreman` es el dueño de estas lentes; `foundry` las usa al diseñar una automatización.

Cada lente es una manera de pensar con carácter propio, pero trabaja con un contrato: una pregunta que la mueve y
algo concreto que entrega. Propone por separado, sin ver a las otras, en no más de diez líneas. Las lentes están para
abrir la cabeza; algunas propuestas van a sobrar, y eso es parte de aprender.

| Lente | La pregunta que la mueve | Entrega | Le tira hacia… |
|---|---|---|---|
| **El vago** | ¿Qué es lo mínimo que llega al resultado? | La opción más barata que funciona, y lo que se pierde con ella | Abajo en la escalera |
| **El optimista** | ¿Y si sale todo bien y lo llevamos al máximo? | El techo, rotulado como techo, y qué tendría que ser cierto para llegar | Arriba en la escalera |
| **El creativo** | ¿De qué otras formas se puede resolver? | Tres o más caminos realmente distintos, no variantes del mismo | Hacia los costados |
| **El meticuloso** | ¿Qué se rompe y cómo nos enteramos? | Los modos de falla, los casos límite y el control que avisa | Hacia el control |
| **El escéptico** | ¿Vale la pena? ¿Contra qué se compara? | El contrafáctico (seguir a mano, un escalón menos), el umbral y el costo oculto | Hacia no hacer |
| **El innovador** | ¿Qué oficio ya resolvió esto? | Un método o herramienta traído de otra disciplina, con los supuestos que trae | Hacia afuera |
| **El lector** | ¿Cómo lo va a usar quien lo recibe? | Lo que va a entender mal, lo que no va a mirar y el formato que sí va a usar | Hacia el usuario |

## Cómo escribir cada propuesta

- Empezá por la idea, no por el personaje: «Con una búsqueda de menciones y un resumen de tres líneas alcanza», no
  «Como soy vago, …».
- Una propuesta concreta, con su escalón y lo que exige.
- Si la lente no tiene nada útil que decir en este caso, que lo diga en una línea. No se rellena.

## Dónde se despliegan (puntos fijos)

| Punto | Lentes | Por qué ahí |
|---|---|---|
| `foundry`, al diseñar una automatización | vago, optimista, escéptico, meticuloso (+ creativo, innovador, lector si la tarea es nueva o la usa otro) | La tensión entre barato y ambicioso decide |
| Fase 2, en una decisión grande (método, inversión, diseño de un sistema) | creativo, escéptico, optimista, innovador | Se ensanchan las opciones antes de cerrar |
| Fase 6, en una ronda grande | meticuloso (como revisor independiente de `hallmark`), lector | Es el control antes de entregar |
| Modo charla, cuando el usuario quiere ideas | las que pida, o creativo, innovador y optimista | Para salir de la zona de confort |

Fuera de estos puntos no se despliegan: una lente en cada paso es ruido y gasta.

## El registro de lentes

Una fila por propuesta, en el registro que fija la configuración del ambiente:

```markdown
| Fecha | Proyecto | Punto | Lente | Propuesta (una línea) | ¿Se usó? | Por qué |
|---|---|---|---|---|---|---|
```

Con el tiempo muestra qué lente rinde en qué punto. Es un dato para proponer cambios a esta tabla, no para aplicarlos
solo.

## Cuando las lentes van como agentes

El encargo de cada una lleva:
- el contexto confirmado (en `foundry`: el relevamiento, la cuenta de si vale la pena y lo que ya existe; en una
  decisión: la pregunta y las opciones conocidas);
- su fila de la tabla de contratos.

No lleva las propuestas de las demás. Formato de devolución: la propuesta en diez líneas como máximo, su escalón y
su riesgo principal.
