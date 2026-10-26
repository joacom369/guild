# Auditoría de las skills · 2026-10-25

> **Documento histórico** (2026-10-25): registra cómo se llegó al mapa. Lo vigente está en
> [`MAPA.md`](MAPA.md) y en cada skill; si difieren, mandan ellos.

> Registro histórico: usa los nombres de ese día. `criterio-herramientas` hoy se llama `compass`.

Tres miradas independientes:
- **Oficial:** documentación de Claude Code, la consultó un agente especializado.
- **Comunidad:** búsqueda web; la mayoría de las fuentes son secundarias.
- **Revisión independiente:** un modelo fuerte leyó las skills sin ver el plan.

Los hallazgos de la revisión se verificaron contra los archivos antes de anotarlos (marca ✔). Lo que no se pudo
confirmar lo dice.

## 1. Lo que dice la evidencia externa

| Tema | Qué se sabe | Nivel de evidencia | Fuente |
|---|---|---|---|
| El problema es la **activación**, no la elección | Sin ayuda, una skill se activa en ~50 % de los casos en que debería. Con descripción directiva y un hook que obliga a evaluar las skills, ~100 % en 22 pedidos y 75 % en pedidos difíciles | Medido, un autor | scottspence.com (2026-02-08) |
| **Contexto pasivo** contra skills | Un índice en AGENTS.md/CLAUDE.md acertó más que las skills en el conocimiento de marco (100 % contra 79 %, Vercel) | Medido por Vercel; visto sólo en resúmenes | aihola.com, devgenius (2026-01) |
| **Presupuesto del listado** | Las descripciones comparten un tope de contexto. description + when_to_use se cortan a 1.536 caracteres; cuando no entran, se descartan las menos usadas | Oficial + mecánica descrita | code.claude.com/docs/en/skills.md |
| **Solapamiento** | Ante un pedido, preguntarse «¿cuál elegiría yo?». Si hay duda, fusionar o escribir el caso negativo («no para X; usar Y») | Opinión + linter | dev.to/rulestack |
| **Probar el disparo** | `claude plugin eval` con casos y evaluadores; uno de tipo `tool_used: Skill` mide si dispara. Lo recomendado: la mitad de los casos que deberían disparar y la otra mitad, casos parecidos que no | Oficial | code.claude.com/docs/en/plugin-evals.md |
| **Skill que invoca otra skill** | No está documentado. Sí lo está: un subagente con el campo `skills` (precarga hasta 32) y `context: fork` | Oficial | code.claude.com/docs/en/sub-agents.md |
| **Debates y personalidades** | Los debates entre agentes no superan de forma fiable a métodos simples (voto, self-consistency) y pueden empeorar por acuerdo reflejo | Medido, académico | arxiv 2502.08788, NeurIPS 2025, arxiv 2509.05396 |
| **Equipos de agentes** | Subagentes primero. Los equipos son experimentales y multiplican el costo | Opinión de practicantes; el «7x» no se confirmó | medium.com (2026-03) |
| **Worktrees** | Sirven para paralelizar tareas independientes. El conflicto se traslada al merge y el cuello de botella es la revisión humana | Anécdotas | morphllm.com, dev.to |
| **Workflows** | Recomendados para 5 o más agentes que se verifican entre sí. Se guardan en `.claude/workflows/` o dentro de un plugin | Oficial | code.claude.com/docs/en/workflows.md |

## 2. Hallazgos sobre nuestras skills (revisión independiente)

| # | Hallazgo | Gravedad | Verificado |
|---|---|---|---|
| 1 | Las versiones viejas `metodo-riguroso` y `reparto-eficiente` siguen instaladas y compiten por los mismos momentos | Rompe el uso | ✔ (synced/) |
| 2 | CLAUDE.md no nombra `quarry` ni `hallmark`, y repite sus reglas en prosa | Rompe el uso | ✔ |
| 3 | La description de `provenance` reclama los momentos de `quarry`, `criterio-herramientas` y `hallmark` | Confunde | ✔ |
| 4 | La naturaleza de la cifra tiene **cinco vocabularios** distintos (kiln agrega «referencia», otras sacan «reconstruido») | Confunde | ✔ kiln/reference/datos-en-pantalla.md:11 |
| 5 | El papel de `design-taste-frontend` difiere: CLAUDE.md dice «pulir» y kiln, «elegir la dirección» | Confunde | ✔ |
| 6 | «Tablero» dispara seis skills a la vez; la tabla de compañeras de kiln no incluye `criterio-herramientas`, `quarry` ni `dataviz` | Confunde | Parcial (sí la falta en la tabla) |
| 7 | `tokenwise` §4 y §7 duplican reglas de `hallmark` y `quarry` | Menor | ✔ |
| 8 | El protocolo de modelado tiene dos dueños (`criterio-herramientas` y `provenance`) | Confunde | Sin verificar línea por línea |
| 9 | Validación escrita en tres lugares (identidades, lectura, crítica independiente) | Menor | ✔ |
| 10 | Abrir y cerrar sesión (ESTADO.md) sólo existe en una referencia; ninguna description cubre «retomar un proyecto» | Confunde | ✔ |
| 11 | `quarry` no deriva a las skills de dominio de la empresa cuando el origen es uno de sus sistemas | Confunde | ✔ |
| 12 | El revisor del nivel 3 de `hallmark` recibe «corré `cifras.py`» sin ruta; un subagente no lo encuentra | Rompe el uso | ✔ revisor.md:29 |
| 13 | `provenance` (182 líneas) y `tokenwise` (177), las que más se cargan, son las más largas; tokenwise trae datos de modelos que envejecen | Menor | ✔ |
| 14 | `kiln/reference/anti-defaults.md` manda modificar la skill con un commit en medio de una tarea, sin aval | Menor | ✔ :28 |
| 15 | Convenciones mezcladas: `reference/` y `referencias/`, nombres en inglés y en castellano, casos de una empresa dentro de skills generales | Menor | ✔ |

## 3. Lectura de conjunto

- La jerarquía existe **de hecho**: forma de pensar → criterio → procedimientos → dominio. Pero **no está escrita en
  ningún lado**, y `provenance` se presenta como dueña de todos los momentos.
- **Falta un único lugar que fije la secuencia** (plantear → elegir → extraer → calcular → controlar → presentar) y
  quién es dueño de cada regla. Ese lugar es justamente el «cerebro».
- La evidencia externa favorece un **cerebro liviano**: un índice en contexto pasivo (CLAUDE.md o mapa), descripciones
  que no se solapen, un hook si la activación falla y pruebas de disparo. Desaconseja un enjambre de personalidades
  que debaten. Las miradas distintas rinden como **verificación** (pocas, en puntos fijos), no como debate.
