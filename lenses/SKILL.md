---
name: lenses
description: >
  Siete lentes (vago, optimista, creativo, meticuloso, escéptico, innovador y lector) que proponen por separado para
  abrir las opciones antes de decidir. Trae el contrato de cada una, los puntos fijos donde se despliegan, cómo se
  sintetizan y el registro de qué lente aportó qué. Usar cuando un trabajo llega a uno de sus puntos fijos (diseñar
  una automatización, una decisión de método grande, el control de una ronda grande), cuando el usuario pide ideas
  desde ángulos distintos («abrí opciones», «¿qué diría un escéptico?», «pensalo de otras formas»), o con /lenses.
  No decide (decide el usuario) ni reemplaza la revisión independiente de `hallmark`.
license: MIT
---

# Lenses: las lentes

Siete maneras de pensar que sacan el trabajo de su zona de confort: discuten la bibliografía habitual, traen
herramientas de otros oficios y estiran el techo. Rompen la rutina, no las reglas: el escéptico y el meticuloso están
para que lo disruptivo también se pruebe. Algunas propuestas van a sobrar, y eso es parte de aprender.

Esta skill es la dueña de los contratos, los puntos y el registro. La usan `foreman` (en las decisiones de un
trabajo) y `foundry` (al diseñar una automatización).

## Los contratos

Cada lente tiene carácter propio, pero trabaja con un contrato: una pregunta que la mueve y algo concreto que entrega.

| Lente | La pregunta que la mueve | Entrega | Le tira hacia… |
|---|---|---|---|
| **El vago** | ¿Qué es lo mínimo que llega al resultado? | La opción más barata que funciona, y lo que se pierde con ella | Abajo en la escalera |
| **El optimista** | ¿Y si sale todo bien y lo llevamos al máximo? | El techo, rotulado como techo, y qué tendría que ser cierto para llegar | Arriba en la escalera |
| **El creativo** | ¿De qué otras formas se puede resolver? | Tres o más caminos realmente distintos, no variantes del mismo | Hacia los costados |
| **El meticuloso** | ¿Qué se rompe y cómo nos enteramos? | Los modos de falla, los casos límite y el control que avisa | Hacia el control |
| **El escéptico** | ¿Vale la pena? ¿Contra qué se compara? | El contrafáctico (seguir a mano, un escalón menos), el umbral y el costo oculto | Hacia no hacer |
| **El innovador** | ¿Qué oficio ya resolvió esto? | Un método o herramienta traído de otra disciplina, con los supuestos que trae | Hacia afuera |
| **El lector** | ¿Cómo lo va a usar quien lo recibe? | Lo que va a entender mal, lo que no va a mirar y el formato que sí va a usar | Hacia el usuario |

## Dónde se despliegan (puntos fijos)

| Punto | Lentes | Por qué ahí |
|---|---|---|
| Diseñar una automatización (`foundry`) | vago, optimista, escéptico, meticuloso (+ creativo, innovador y lector si la tarea es nueva o la usa otro) | La tensión entre barato y ambicioso decide |
| Fase 2, en una decisión grande (método, inversión, diseño de un sistema) | creativo, escéptico, optimista, innovador | Se ensanchan las opciones antes de cerrar |
| Fase 6, en una ronda grande | meticuloso (como revisor independiente de `hallmark`), lector | Es el control antes de entregar |
| Una charla de ideas, a pedido del usuario | las que pida, o creativo, innovador y optimista | Para salir de la zona de confort |

Fuera de estos puntos no se despliegan: una lente en cada paso es ruido y gasta.

## Cómo se proponen

- **Por separado:** cada lente escribe sin ver a las otras, en no más de diez líneas.
- Empezá por la idea, no por el personaje: «Con una búsqueda de menciones y un resumen de tres líneas alcanza», no
  «Como soy vago, …».
- Una propuesta concreta, con lo que exige y su riesgo principal.
- Si la lente no tiene nada útil que decir en este caso, lo dice en una línea. No se rellena.

**En el mismo turno o como agentes.** Por defecto, cada lente es un bloque aparte en el mismo turno: es lo barato y
alcanza en lo chico. Como agentes separados (no se contaminan entre sí, que es el punto) cuando la decisión es grande;
el pedido de agentes sigue `tokenwise`. El encargo de cada una lleva el contexto confirmado y su fila de contratos,
nunca las propuestas de las demás; devuelve la propuesta en diez líneas, lo que exige y su riesgo principal.

## Cómo se sintetizan

Quien convocó a las lentes (`foreman` o `foundry`) arma **dos o tres opciones** con lo que propusieron, cada una con
la lente que la originó. Recomienda una y dice por qué. **Decide el usuario.**

## El registro

Una fila por propuesta, en el registro de lentes que fija la configuración del ambiente:

```markdown
| Fecha | Proyecto | Punto | Lente | Propuesta (una línea) | ¿Se usó? | Por qué |
|---|---|---|---|---|---|---|
```

Con el tiempo muestra qué lente rinde en qué punto. Es un dato para **proponer** cambios a esta skill, no para
aplicarlos solo.
