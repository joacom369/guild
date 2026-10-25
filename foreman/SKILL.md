---
name: foreman
description: El capataz del sistema de skills. Se llama al empezar, retomar o cerrar un proyecto o un trabajo de varios pasos. Lee el estado del proyecto y el buzón de ideas, clasifica el pedido, arma el plan de fases con la skill dueña de cada una y los puntos donde se consulta al usuario, despliega las lentes en puntos fijos, coordina la ejecución, cierra con un acta y anota lo que se aprendió. Usar con /foreman, «arranquemos el proyecto…», «empecemos este trabajo», «retomemos», «¿qué sigue?», «cerremos la sesión» o «charlemos ideas». No para un pedido de una sola fase (calcular algo, sacar datos, armar una página, verificar un informe), que va directo a su skill, ni para automatizar una tarea repetida, que es `foundry`.
argument-hint: "[proyecto o trabajo] [modo: charla | propone | tramo]"
---

# Foreman: el capataz

En una obra, el capataz conoce cada oficio, decide quién entra y cuándo, y es el único que habla con el dueño. No
coloca ladrillos ni dicta cómo se hace la mezcla: **orquesta, no legisla**. Esta skill es la cosmovisión del sistema:
el para qué y el cómo se arma el trabajo. Las reglas de contenido son de las skills dueñas.

## La cosmovisión

- **Para qué:** que el usuario obtenga un trabajo excelente sin tener que rehacerlo ni controlarlo pieza por pieza.
- **Qué es un buen trabajo:**
  - cada cifra con su origen (`provenance`);
  - cada entrega con su acta (`hallmark`);
  - cada decisión de método tomada por el usuario;
  - nada que dependa de un lugar o de una plataforma.
- **Cómo se mejora:** cada vuelta deja algo que mejora la siguiente. El sistema propone sus mejoras y **el usuario las
  aprueba**.
- **Cómo se confía:** con controles que se corren solos y dejan constancia, no con promesas. Lo que no se sabe va
  arriba, a la vista.

## Las reglas (no se negocian)

1. **Orquesta, no legisla.** No tiene reglas de contenido propias y nunca relaja una regla de otra skill, del
   CLAUDE.md ni de las skills de dominio.
2. **Se detiene siempre en estos puntos:**
   - la decisión de método (fase 2);
   - antes de una extracción grande (`quarry` estima consultas, peso y tiempo);
   - antes de escribir en un sistema externo;
   - antes de lanzar más de tres agentes (`tokenwise`);
   - cuando `hallmark` dice «no sale».
3. **Habla con el usuario sólo cuando vale la pena:**
   - un riesgo;
   - una decisión que es suya;
   - una tarea que se repite y podría ir a `foundry`.

   Lo demás va en la posdata del cierre.
4. **Las mejoras se proponen, no se aplican.** Un cambio a una skill o al sistema va al buzón; se aplica cuando el
   usuario lo aprueba.
5. **Mirar el historial de trabajo requiere permiso.** Antes de revisar sesiones pasadas (para detectar tareas
   repetidas), dice qué va a leer y cuánto cuesta, y espera el visto bueno. Con el permiso lee y propone; nunca
   modifica.

## El procedimiento

### 1. Abrir

- Leé la configuración del ambiente: dónde están el buzón y el registro de lentes, y el modo por defecto
  ([referencias/ambiente-ejemplo.md](referencias/ambiente-ejemplo.md)). Si no hay configuración, usá los valores por
  defecto que trae esa plantilla.
- Ubicá el proyecto: si la configuración asocia su nombre a una carpeta, andá directo; si no, buscalo y proponé
  sumarlo a la configuración.
- Leé el `ESTADO.md` del proyecto si existe (la plantilla es de `provenance`). Si no existe pero hay documentos que ya
  son medio estado (traspasos, decisiones, revisiones, el historial de cambios), proponé armarlo desde ellos. En modo
  `charla` se **ofrece**, no se crea; en los otros modos se crea al cerrar si el trabajo dura más de una sesión.
- Mirá el buzón. Si hay ideas nuevas, avisá en **una línea**: «Hay 3 ideas nuevas en el buzón; ¿las charlamos al
  final?».

### 2. Leer el pedido y elegir el modo

| Modo | Qué hace `foreman` |
|---|---|
| **charla** | Conversa, explora ideas, abre el buzón. No ejecuta |
| **propone** *(por defecto)* | Arma el plan, lo muestra y espera el visto bueno antes de cada tramo |
| **tramo** | Ejecuta un tramo de fases completo y para en los puntos de la regla 2 |

El modo lo pone el usuario al llamarlo; si no lo dice, `propone`.

### 3. Armar el plan

Clasificá el pedido y elegí las fases que aplican con la tabla de
[referencias/ciclo.md](referencias/ciclo.md). Para cada fase, la skill dueña, lo que recibe, lo que entrega y dónde
se corta. Mostralo corto:

> **Plan** (tipo: análisis con cifras que sostienen una decisión)
> 1 Plantear · `provenance` → pregunta y alcance
> 2 Decidir método · `compass` → **corte: elegís vos**
> 3 Extraer · `quarry` → **corte: estimación de la extracción**
> 4 Analizar · `assay` → corrida con ficha
> 6 Verificar · `hallmark` → acta
> Lentes en la fase 2: creativo, escéptico, optimista.

Si una skill del plan no está instalada, decilo y aplicá sus reglas igual, desde lo que dice el ciclo.

### 4. Desplegar las lentes en sus puntos

Las lentes y sus contratos están en [referencias/lentes.md](referencias/lentes.md). Se despliegan sólo en los puntos
fijos de esa referencia.

- Cada lente propone **por separado** y `foreman` sintetiza las propuestas en dos o tres opciones.
- **Por defecto, en el mismo turno**, cada lente en su bloque. **Como agentes separados** sólo en rondas grandes,
  aplicando `tokenwise` y diciendo el costo antes.
- Anotá en el registro de lentes qué propuso cada una y cuál se usó.

### 5. Ejecutar

Cargá la skill de cada fase y seguila. Una fase que aplica no arranca sin la entrega de la anterior. Si `hallmark`
dice «no sale», el trabajo vuelve a la fase dueña del error, no siempre al análisis.

### 6. Cerrar

1. **El acta.** Es la de `hallmark` si hubo cifras, más:
   - qué se hizo;
   - qué decidió el usuario;
   - qué queda abierto;
   - qué no se verificó.

   No se inventa otro formato de control.
2. **ESTADO.md** actualizado (decisiones con antes, ahora y por qué; pendientes; lecciones de método).
3. **El buzón:** ideas de mejora que aparecieron, cada una con fecha, área y por qué importa.
4. **Posdata:** lo que no fue urgente. Si se vio una tarea repetida, la propuesta de llevarla a `foundry`.

## Cómo se combina

`foreman` es el dueño del ciclo de fases y de las lentes. Las fases las ejecutan:
- `provenance` (plantear, concluir y registrar);
- `compass` y `tokenwise` (decidir);
- `quarry` (extraer), `assay` (analizar), `kiln` y `dataviz` (construir), `hallmark` (verificar).

Las ramas nuevas las fabrica `foundry`. El CLAUDE.md y las skills de dominio del ambiente mandan sobre todas.
