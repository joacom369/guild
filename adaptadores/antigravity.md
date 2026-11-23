# Adaptador: Google Antigravity (2.0 / IDE / CLI)

Diseñado y documentado el **2026-11-23**. **Parcialmente probado** en Antigravity 2.0 (Windows): se probaron la instalación global de los 12 oficios propios en `~/.gemini/config/skills/`, su carga progresiva por `description`, la lectura de modelos y cuotas con `swarm` (`action: "models"`), y la ejecución de scripts Python locales (Python 3.14). El resto (hook `SessionStart`, `swarm` con workers activos, `run_workflow`, `schedule`, MCP propios) queda marcado **documentado** hasta probarse en un trabajo real.

El núcleo no nombra a Antigravity ni copia sus límites de concurrencia o pools. Las diferencias de la plataforma viven en este archivo.

## Instalar

- **Global (probado):** copiar las carpetas de los oficios propios (`foreman`, `provenance`, `compass`, `tokenwise`, `lenses`, `quarry`, `assay`, `kiln`, `hallmark`, `herald`, `foundry`, `sherpa`) en `~/.gemini/config/skills/<oficio>/`, excluyendo `evals/` y `__pycache__/` (mismo criterio que [`../empaquetar.py`](../empaquetar.py)). Antigravity las descubre automáticamente al siguiente turno.
- **Por proyecto (documentado):** `.agents/skills/` o `skills.json` en la raíz del repositorio.
- **Reglas siempre activas (documentado):** `GEMINI.md` o `AGENTS.md` jerárquicos (límite de **24.000 bytes** por archivo y presupuesto agregado de **20.000 tokens**; las reglas que superan el presupuesto se degradan a punteros de ruta).
- **Plugins (documentado):** alternativa para empaquetar oficios + reglas + MCP en `~/.gemini/config/plugins/<nombre>/plugin.json`. Nunca editar `~/.gemini/config/config.json` a mano.
- **Manifiestos multi-plataforma (documentado):** este repo incluye [`.agents/skills.json`](../.agents/skills.json) (heredable desde `~/.gemini/config/skills.json` sin copiar carpetas) y manifiestos para Codex y Cursor. No se agrega `plugin.json` en la raíz porque Antigravity espera las skills dentro de `skills/<oficio>/`, mientras `Guild` las mantiene en la raíz para compatibilidad con Claude Code.

## Cómo resuelve el contrato

| Necesidad del núcleo | En Google Antigravity | Estado |
|---|---|---|
| Saber qué oficio cargar y cuándo | `description` con carga progresiva en `~/.gemini/config/skills/` + índice en `GEMINI.md` / `AGENTS.md` | probado (skills) / documentado (índice) |
| Cargar un procedimiento a demanda | Skill (`SKILL.md` y `referencias/`) desde `~/.gemini/config/skills/` o `.agents/skills/` | probado |
| Reglas que valen siempre | `GEMINI.md` / `AGENTS.md` jerárquicos (24.000 bytes/archivo, 20.000 tokens agregados) | documentado |
| Algo que pasa al abrir la sesión | `hooks.json` evento `SessionStart` (`type: "command"`, devuelve `injectSteps` → `systemMessage` en JSON camelCase; **no instalado**: es decisión del usuario) | documentado |
| Agente con una tarea | `invoke_subagent` (4 alias: `inherit`, `flash_lite`, `flash`, `pro`; `research` sin red; `browser` en `flash`) o `swarm` (23 IDs explícitos modelo+esfuerzo, `workspace: inherit\|share\|branch`, cambio en caliente con `action: "model"`) | documentado (`swarm models` probado) |
| Varios agentes en un orden fijo | `run_workflow` (Python: `agent`, `parallel`, `pipeline`, `phase`) o `swarm` con tablero compartido | documentado |
| Correr solo, con horario | `schedule` (`CronExpression` de 5 campos + `IsDaemon: true` para tareas permanentes; timers con `DurationSeconds`) | documentado |
| Conectores del usuario | `mcp_config.json` (global o en plugin; placeholders `${X}` declarados en `variables`, no expande env del SO) + verificación de identidad con receta de `quarry` | documentado |
| Pasos mecánicos | Los mismos scripts Python | probado |

## Pools de cuota y catálogo de modelos (observado el 2026-11-23)

**Lo que NO está publicado (arriba a la vista):**
- Multiplicadores exactos de `%` de cuota por modelo y nivel de esfuerzo (los precios API en USD se citan sólo como **proxy relativo**, supuesto).
- Mapeo interno exacto de los alias `flash_lite`, `flash` y `pro` de `invoke_subagent`.
- Precio oficial en `ai.google.dev` de `Gemini 4 Argon` (sólo hallado en fuentes secundarias: USD 2,00 / USD 10,00 promo → USD 4,00 / USD 20,00 estándar por 1M).
- Ahorro exacto de `Orchestrator (Neon)` frente a `Neon` solo en esta instancia.
- Techo semanal absoluto sobre los pools de ~5h (`swarm models` muestra `%` libre y próximo reset, no el acumulado semanal).

**Tres pools independientes observados vía `swarm models` (23 endpoints):**

- **Pool 1 (ventana corta ~5h):**
  - `Claude Opus 5.5` (Low / Medium / High): 1M entrada / 128K salida, pensamiento adaptativo (default `medium`), API USD 4,00 / USD 20,00 por 1M, cache read USD 0,20 (`claude.com`, `anthropic.com`).
  - `Claude Sonnet 5.5` (Low / Medium / High): 1M entrada / 128K salida, pensamiento adaptativo, API USD 2,00 / USD 10,00 por 1M, cache read USD 0,10 (`claude.com`, `anthropic.com`).
  - `GPT-OSS 120B` (Medium): MoE abierto (117B total / ~5,1B activos, `openai.com`), retirado de listas generales según `google.dev`; comparte pool con Claude → evitar.
- **Pool 2 (ventana corta ~5h):**
  - `Gemini 3.8 Flash` (Low / Medium / High): 1M entrada / 64K salida separadas, API USD 0,75 / USD 3,75 intro → USD 1,50 / USD 7,50 estándar; Terminal-Bench 2.1: 90,8%, SWE-Bench Pro: 61,6%, SWE-Atlas: 51,9%, Terminal-Bench 4.1: 18,2% (`google.com`, `blog.google`).
  - `Gemini 4 Hydrogen` (Low / Medium / High / XHigh): 1M unificada, API USD 1,50 / USD 7,50 por 1M, cache implícito USD 0,075; Terminal-Bench 4.1: ~57%, ~2,5× más rápido y >5× menos alucinaciones que 3.8 Flash (`blog.google`, `google.com`).
  - `Gemini 4 Neon` (Low / Medium / High / XHigh): 1M unificada, API USD 3,00 / USD 15,00 por 1M, cache implícito USD 0,15; Terminal-Bench 4.1 (ajust.): 65,2%, FrontierCode 2.0 (high): 46,2%, SWE-sweep en Antigravity: 39,0% (`blog.google`, `deepmind.google`).
  - `Orchestrator (Neon)`.
- **Pool 3 (ventana larga ~5 días):**
  - `Gemini 4 Argon` (Low / Medium / High): salida ampliada a 1M; DeepSWE v1.1: 77,9%, Terminal-Bench 4.0: ~57,4%, ERQA: 87% (`blog.google`, `deepmind.google`, `googleblog.com`).
  - `Orchestrator (Argon)`.

*(Observación: `Gemini 4 Carbon` figura en publicaciones de Google pero no está expuesto entre los 23 endpoints de esta instancia. Sobre **Orchestrator**: empareja un planificador —`Neon` o `Argon`— con un ejecutor rápido —`Hydrogen`—; la referencia publicada por Google, medida frente a Carbon solo, reporta éxito cercano a frontera con ~24% menos cuota y ~19% más rápido — `blog.google`, `antigravity.google`, **preliminar sobre referencias** para `Neon`/`Argon`.)*

## Distribución costo/beneficio por oficio (aprobada el 2026-11-23 · nivel preliminar sobre referencias)

| Oficio / Fase (`guild`) | Mecanismo en Antigravity | Modelo y esfuerzo recomendado | Pool | Cuándo escalar / alternativa |
|---|---|---|---|---|
| **Abrir / Planear / Cerrar** (`foreman`, `provenance`, `compass`) | Sesión principal (`main` u `Orchestrator`) | **`Orchestrator (Neon)`** *(o `Neon Medium` en charla)* | Pool 2 (~5h) | Si la arquitectura abarca todo un repo o falla 2 veces → **`Orchestrator (Argon)`** *(Pool 3)* |
| **Lentes en Fase 2** (`lenses`) | En el mismo turno (chico) · `swarm` sólo en decisión grande | En turno: hereda `foreman` · En `swarm`: **`Hydrogen (Medium)`** o **`Sonnet 5.5 (Medium)`** | Pool 2 o 1 | Nunca `Opus` ni `Argon` para las 4 lentes en paralelo |
| **Extraer / Investigar** (`quarry`, `sherpa`, relevamientos) | Directo si es chico · `invoke_subagent` (`research`/`browser`) o `swarm` si hay ≥3 fuentes independientes | **`Gemini 4 Hydrogen (Low / Medium)`** *(o `flash` en `browser`)* | Pool 2 (~5h) | Si hay >5 fuentes homogéneas, `run_workflow` con workers en `Hydrogen (Low)` |
| **Analizar / Modelar** (`assay`) | Sesión principal (`Orchestrator`) o worker aislado si corre aparte | **`Orchestrator (Neon)`** o **`Gemini 4 Neon (High)`** | Pool 2 (~5h) | Problemas matemáticos/estadísticos duros tras fallo → **`Neon (XHigh)`** o **`Argon (High)`** *(Pool 3)* |
| **Construir código / UI / entregables** (`kiln`, código) | `Orchestrator (Neon)` en serie · `swarm` con `workspace: "share"` si hay módulos independientes | Plan: **`Neon`** · Ejecución: **`Hydrogen (Medium/High)`** | Pool 2 (~5h) | Ediciones mecánicas o tests con verificación automática: **`Hydrogen (Low/Medium)`** y escalar sólo si falla el test |
| **Verificar / Auditor externo** (`hallmark` nivel 3) | `swarm` (worker limpio sin ver el plan, **otra familia**) | **`Claude Sonnet 5.5 (High)`** *(ronda normal)* · **`Claude Opus 5.5 (Medium/High)`** *(ronda crítica)* | **Pool 1 (~5h)** | Si Pool 1 está bajo → **`Gemini 4 Argon (High)`** *(Pool 3)* |
| **Escrituras externas** (`herald`) | Directo en sesión principal, siempre con vista previa y aprobación | Hereda `foreman` (nunca delegar escritura o borrado a subagente autónomo) | Pool 2 | — |
| **Rutinas programadas** (`foundry` / `sherpa`) | `schedule` (`IsDaemon: true`) | **`Gemini 4 Hydrogen (Low/Medium)`** | Pool 2 (~5h) | Evitar modelos pesados en cron recurrente |

**Cuatro reglas prácticas del reparto:**
1. **`Hydrogen` reemplaza a `3.8 Flash` en Pool 2** para tareas agénticas (salvo que la calibración empírica demuestre un ahorro de `%` suficiente para lecturas triviales).
2. **`Pool 3 (Argon)` es reserva estratégica (~5 días)**, no modelo de uso diario.
3. **`Pool 1 (Claude 5.5)` sirve como auditor independiente de otra familia** (`hallmark` nivel 3) sin drenar Pools 2 ni 3; no usar `GPT-OSS 120B`.
4. **Escalado por esfuerzo antes que salto de modelo:** arrancar en `Low`/`Medium` (o `Orchestrator (Neon)`); `XHigh` sólo tras fallo verificado. Aprovechar caching implícito (>4.096 tokens en Gemini 4, hasta 95% de descuento) manteniendo sesiones estables y configurando `.antigravityignore` en proyectos grandes.

**Calibración empírica en `~/.foreman/DELEGACIONES.md`:** al cerrar cada delegación o ronda sustancial, anotar `pool`, `modelo/esfuerzo`, `% antes → % después` (leído de `swarm models` o `/usage`) y si hubo retrabajo, para pasar la matriz de *preliminar sobre referencias* a *observado*.

## Lo que no da igual (límites de plataforma)

- **`invoke_subagent` vs `swarm`:** `invoke_subagent` sólo expone 4 alias (`inherit`, `flash_lite`, `flash`, `pro`), `research` corre sin acceso a red y `browser` usa `flash` por defecto. `swarm` permite elegir cualquiera de los 23 IDs explícitos y cambiar de modelo en caliente (`action: "model"`) conservando la conversación. Los workers en paralelo multiplican el consumo instantáneo del pool; en `waiting` cuestan 0.
- **`herald` no se delega:** ninguna escritura externa ni borrado se ejecuta desde un subagente o worker autónomo.
- **Sandbox de terminal y Windows PowerShell 5.1:** `gh` necesita salir del sandbox (red y keyring). En PowerShell 5.1: (a) `Get-Content` sin `-Encoding UTF8` más `Out-File` —o redirecciones con `>`— corrompen archivos UTF-8 sin BOM (usar `[IO.File]::ReadAllText`/`WriteAllText` con `[Text.UTF8Encoding]::new($false)` o Python con `encoding="utf-8"`); (b) no nombrar `R` a una función auxiliar (choca con el alias de `Invoke-History` y falla en silencio; usar nombres largos); (c) no usar comillas dobles dentro de `--jq`; y (d) la skill externa `pptx` (`scripts/office/validate.py`) falla en Windows al no encontrar sus esquemas XSD (verificar abriendo en PowerPoint o corriendo en Linux/WSL y declararlo en el acta de `hallmark`).
- **Documentación viva (`llms.txt` / MCP `search_docs`):** antes de escribir código contra APIs o SDKs que cambian rápido (Antigravity, `google-genai`, etc.), consultar `https://antigravity.google/llms.txt` (o el `llms.txt` del proveedor) o la herramienta MCP de documentación si está activa, en lugar de depender de memoria o inflar skills.
- **`hooks.json`:** sólo soporta `type: "command"` y corre de forma síncrona (bloquea el loop del agente; timeout por defecto de 30 s).
- **Sin `claude plugin eval`:** las pruebas de disparo de `evals/` siguen en Claude Code; el control estático local es `python foundry/scripts/auditar_gremio.py`.

## Hook de inicio de sesión (opcional, sin instalar ni probar)

Para que Antigravity avise al abrir una sesión si hay ideas nuevas en `~/.foreman/IDEAS.md`, se puede declarar en `hooks.json` (el ejemplo está documentado, **no instalado ni probado**):

```json
{
  "foreman-buzon": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python -c \"import json,pathlib,sys;sys.stdout.reconfigure(encoding='utf-8');p=pathlib.Path.home()/'.foreman'/'IDEAS.md';n=sum('| nueva |' in l for l in p.read_text(encoding='utf-8').splitlines()) if p.exists() else 0;print(json.dumps({'injectSteps':[{'systemMessage':{'systemMessage':f'foreman: hay {n} ideas nuevas en el buzón'}}]} if n else {}, ensure_ascii=False))\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Checklist para marcar «probado»

- [ ] Cargar el índice en `GEMINI.md` / `AGENTS.md` y confirmar disparo correcto de los oficios en una sesión real.
- [ ] Instalar y probar el hook `SessionStart` en `hooks.json` verificando el aviso de buzón al iniciar conversación.
- [ ] Correr un `swarm` con auditor independiente en Pool 1 (`Claude Sonnet 5.5 High`) registrando `pool`, `modelo/esfuerzo` y `% antes → % después` en `~/.foreman/DELEGACIONES.md`.
- [ ] Probar una rutina programada (`schedule` con `IsDaemon: true`) para `sherpa` o auditoría periódica.
- [ ] Conectar un servidor MCP en `mcp_config.json` y verificar la identidad de la cuenta con una lectura real (`quarry`).
