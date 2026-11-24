"""Captura una página en escritorio y celular con Chrome/Edge headless, sondea calidad AAA y prueba interacciones.

Uso:
    python foto_pagina.py URL PREFIJO [--selector CSS] [--espera 3] [--oscuro]
                          [--escritorio 1440x900] [--celular 390x844] [--limite 90]
                          [--interacciones PLAN.json] [--json REPORTE.json]
                          [--sin-sonda] [--estricto]

Escribe PREFIJO-escritorio.png y PREFIJO-celular.png (la página entera, o sólo el selector si se pasa).
Sonda automática (desactivable con --sin-sonda): errores de consola, HTTP >= 400, imágenes rotas, enlaces muertos,
controles tapados, targets < 44 px en celular, controles sin nombre en AXTree y opacidad 0 con reduced-motion.
Con --interacciones ejecuta un plan JSON (click/fill/focus/key/wait) y verifica estado resultante.
Con --estricto sale con código 1 ante cualquier defecto o fallo de interacción.
"""
import argparse
import asyncio
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CANDIDATOS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser", "microsoft-edge",
]

ROLES_CON_NOMBRE = {
    "button", "link", "textbox", "checkbox", "switch",
    "tab", "combobox", "slider", "menuitem",
}

TECLAS = {
    "Escape": ("Escape", "Escape", 27, ""),
    "Tab": ("Tab", "Tab", 9, ""),
    "Enter": ("Enter", "Enter", 13, "\r"),
    "Space": (" ", "Space", 32, " "),
    "ArrowRight": ("ArrowRight", "ArrowRight", 39, ""),
    "ArrowLeft": ("ArrowLeft", "ArrowLeft", 37, ""),
    "ArrowDown": ("ArrowDown", "ArrowDown", 40, ""),
    "ArrowUp": ("ArrowUp", "ArrowUp", 38, ""),
}

JS_SONDA = r"""
((esMovil) => {
  const oculto = (el) => {
    if (!el || el.nodeType !== 1) return true;
    if (el.closest('[hidden], [aria-hidden="true"], template, dialog:not([open])')) return true;
    const det = el.closest('details');
    if (det && !det.open && !el.closest('summary')) return true;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return true;
    return false;
  };
  const etiqueta = (el) => {
    const raw = el.innerText || el.getAttribute('aria-label') || el.getAttribute('alt') || el.getAttribute('title') || el.id || el.tagName;
    const t = String(raw || '').trim().replace(/\s+/g, ' ');
    return t.slice(0, 60) || el.tagName.toLowerCase();
  };
  const imagenes_rotas = [];
  for (const img of document.querySelectorAll('img')) {
    if (oculto(img)) continue;
    if (!img.complete || img.naturalWidth === 0) {
      imagenes_rotas.push(img.getAttribute('src') || img.getAttribute('alt') || '(img)');
    }
  }
  const enlaces_muertos = [];
  for (const a of document.querySelectorAll('a')) {
    if (oculto(a)) continue;
    const href = (a.getAttribute('href') || '').trim();
    if (!href || href === '#' || href === '#!' || href.toLowerCase().startsWith('javascript:')) {
      enlaces_muertos.push(`${etiqueta(a)} (${href || 'sin href'})`);
    }
  }
  const controles_tapados = [];
  const targets_chicos = [];
  const selInt = 'button, a[href], [role="button"], [role="tab"], input:not([type="hidden"]), select, textarea, summary';
  for (const el of document.querySelectorAll(selInt)) {
    if (oculto(el) || el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.top >= 0 && r.left >= 0 && r.bottom <= window.innerHeight && r.right <= window.innerWidth && r.width >= 4 && r.height >= 4) {
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const hit = document.elementFromPoint(cx, cy);
      if (hit && hit !== el && !el.contains(hit) && !hit.contains(el)) {
        controles_tapados.push(`${etiqueta(el)} tapado por ${etiqueta(hit)}`);
      }
    }
    if (esMovil) {
      const cs = getComputedStyle(el);
      const esLinkInline = el.tagName === 'A' && cs.display === 'inline' && !!el.closest('p, li, dd, figcaption');
      const esOffscreen = (cs.position === 'absolute' || cs.position === 'fixed')
        && (r.right <= 0 || r.bottom <= 0)
        && document.activeElement !== el;
      if (!esLinkInline && !esOffscreen && (r.width < 44 || r.height < 44)) {
        targets_chicos.push(`${etiqueta(el)} (${Math.round(r.width)}x${Math.round(r.height)})`);
      }
    }
  }
  const opacidad_cero = [];
  for (const el of document.querySelectorAll('section, article, main > *, [data-animate], .reveal')) {
    if (oculto(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width <= 20 || r.height <= 20) continue;
    if (parseFloat(getComputedStyle(el).opacity) === 0) {
      opacidad_cero.push(etiqueta(el));
    }
  }
  return {imagenes_rotas, enlaces_muertos, controles_tapados, targets_chicos, opacidad_cero};
})
"""

JS_VISIBILIDAD = r"""
(sel) => {
  const els = Array.from(document.querySelectorAll(sel));
  if (!els.length) return {presente: false, visible: false, count: 0, texto: ""};
  let visibles = 0;
  for (const el of els) {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const dlgCerrado = el.tagName === 'DIALOG' ? !el.open : !!el.closest('dialog:not([open])');
    if (!el.closest('[hidden]') && !dlgCerrado && cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0 && r.width > 0 && r.height > 0) {
      visibles++;
    }
  }
  return {presente: true, visible: visibles > 0, count: visibles, total: els.length, texto: (els[0].innerText || '').trim()};
}
"""

JS_SNAPSHOT = r"""
(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const attrs = Array.from(el.attributes).filter(a => a.name.startsWith('aria-') || a.name.startsWith('data-') || a.name === 'open' || a.name === 'class').map(a => `${a.name}=${a.value}`).sort();
  return JSON.stringify({text: el.innerText || '', val: el.value || '', len: el.outerHTML.length, attrs});
}
"""


def navegador():
    for c in CANDIDATOS:
        ruta = c if os.path.isfile(c) else shutil.which(c)
        if ruta:
            return ruta
    raise SystemExit("No encontré Chrome, Chromium ni Edge.")


def _cargar_websockets():
    try:
        import websockets
        return websockets
    except ImportError:
        raise SystemExit("Falta la dependencia 'websockets'. Instalala con: pip install websockets")


def _ignorar_url(url):
    return url.split("?", 1)[0].rstrip("/").endswith("/favicon.ico")


async def ax_sin_nombre(cmd, ax_result):
    sin_nombre = []
    for nodo in ax_result.get("nodes", []):
        if nodo.get("ignored"):
            continue
        rol = (nodo.get("role") or {}).get("value", "")
        if rol not in ROLES_CON_NOMBRE:
            continue
        nombre = ((nodo.get("name") or {}).get("value") or "").strip()
        if not nombre:
            sel = ""
            bid = nodo.get("backendDOMNodeId")
            if bid:
                try:
                    info = (await cmd("DOM.describeNode", {"backendNodeId": bid})).get("node", {})
                    tag = (info.get("localName") or info.get("nodeName") or "").lower()
                    attrs = info.get("attributes") or []
                    pares = dict(zip(attrs[0::2], attrs[1::2]))
                    id_ = f"#{pares['id']}" if pares.get("id") else ""
                    cls = "".join(f".{c}" for c in pares.get("class", "").split()[:2])
                    sel = f" ({tag}{id_}{cls})" if tag else ""
                except Exception:
                    sel = ""
            sin_nombre.append(f"role={rol}{sel}")
    return sin_nombre


async def ejecutar_interacciones(cmd, js, plan):
    resultados = []
    for idx, paso in enumerate(plan.get("pasos", []), 1):
        nombre = paso.get("nombre") or f"paso {idx}"
        op = paso.get("op", "")
        sel = paso.get("selector")
        esperar = paso.get("esperar") or {}
        snap_antes = None
        if esperar.get("changed"):
            snap_antes = await js(f"({JS_SNAPSHOT})({json.dumps(esperar['changed'])})")

        err_op = None
        if op == "wait":
            await asyncio.sleep(float(paso.get("ms", 200)) / 1000.0)
        elif op in ("click", "focus", "fill"):
            if not sel:
                err_op = "falta 'selector'"
            else:
                val = json.dumps(str(paso.get("valor", "")))
                res = await js(f"""(() => {{
                    const el = document.querySelector({json.dumps(sel)});
                    if (!el) return "no existe selector: " + {json.dumps(sel)};
                    if (el.disabled) return "elemento deshabilitado";
                    if ({json.dumps(op)} === "click") {{
                        el.scrollIntoView({{block: "center"}});
                        el.click();
                    }} else if ({json.dumps(op)} === "focus") {{
                        el.scrollIntoView({{block: "center"}});
                        el.focus();
                    }} else {{
                        el.scrollIntoView({{block: "center"}});
                        el.focus();
                        el.value = {val};
                        el.dispatchEvent(new Event("input", {{bubbles: true}}));
                        el.dispatchEvent(new Event("change", {{bubbles: true}}));
                    }}
                    return "OK";
                }})()""")
                if res != "OK":
                    err_op = str(res)
        elif op == "key":
            tecla = paso.get("tecla", "")
            key, code, vk, txt = TECLAS.get(tecla, (tecla, tecla, ord(tecla[0].upper()) if len(tecla) == 1 else 0, tecla if len(tecla) == 1 else ""))
            if not key:
                err_op = "falta 'tecla'"
            else:
                base = {"key": key, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
                await cmd("Input.dispatchKeyEvent", {"type": "keyDown", **({"text": txt} if txt else {}), **base})
                await cmd("Input.dispatchKeyEvent", {"type": "keyUp", **base})
        else:
            err_op = f"operación no soportada: {op}"

        await asyncio.sleep(float(paso.get("despues_ms", 120)) / 1000.0)
        fallos = [err_op] if err_op else []

        if not fallos and esperar:
            if "visible" in esperar:
                st = await js(f"({JS_VISIBILIDAD})({json.dumps(esperar['visible'])})")
                if not (st and st.get("visible")):
                    fallos.append(f"esperaba visible {esperar['visible']}")
            if "hidden" in esperar:
                st = await js(f"({JS_VISIBILIDAD})({json.dumps(esperar['hidden'])})")
                if st and st.get("visible"):
                    fallos.append(f"esperaba oculto {esperar['hidden']}")
            if "text_contains" in esperar:
                tc = esperar["text_contains"]
                st = await js(f"({JS_VISIBILIDAD})({json.dumps(tc['selector'])})")
                txt = (st or {}).get("texto", "")
                if tc["text"] not in txt:
                    fallos.append(f"no contiene {tc['text']!r} en {tc['selector']}")
            if "attr" in esperar:
                at = esperar["attr"]
                actual = await js(f"document.querySelector({json.dumps(at['selector'])})?.getAttribute({json.dumps(at['name'])})")
                if actual != at["value"]:
                    fallos.append(f"{at['selector']}[{at['name']}] = {actual!r}, esperaba {at['value']!r}")
            if "focused" in esperar:
                ok_f = await js(f"(() => {{ const e = document.querySelector({json.dumps(esperar['focused'])}); return !!e && (document.activeElement === e || e.contains(document.activeElement)); }})()")
                if not ok_f:
                    fallos.append(f"foco no está en {esperar['focused']}")
            if "count_min" in esperar:
                cm = esperar["count_min"]
                st = await js(f"({JS_VISIBILIDAD})({json.dumps(cm['selector'])})")
                cnt = (st or {}).get("count", 0)
                if cnt < int(cm["min"]):
                    fallos.append(f"visibles en {cm['selector']} = {cnt}, esperaba >= {cm['min']}")
            if "changed" in esperar:
                snap_despues = await js(f"({JS_SNAPSHOT})({json.dumps(esperar['changed'])})")
                if snap_despues == snap_antes:
                    fallos.append(f"sin cambio en {esperar['changed']}")

        resultados.append({"paso": nombre, "ok": not fallos, "detalle": "; ".join(fallos)})
    return resultados


async def capturar(ws_mod, ws_url, url, salida, ancho, alto, a, es_celular, plan_interacciones=None):
    errores, http_errores, req_urls, n = [], [], {}, 0
    async with ws_mod.connect(ws_url, max_size=2 ** 28) as ws:
        async def cmd(metodo, params=None):
            nonlocal n
            n += 1
            mio = n
            await ws.send(json.dumps({"id": mio, "method": metodo, "params": params or {}}))
            while True:
                m = json.loads(await ws.recv())
                method = m.get("method")
                if method == "Runtime.exceptionThrown":
                    d = m["params"]["exceptionDetails"]
                    errores.append(d.get("exception", {}).get("description", d.get("text", ""))[:300])
                elif method == "Runtime.consoleAPICalled" and m["params"]["type"] == "error":
                    errores.append(" ".join(str(x.get("value", x.get("description", ""))) for x in m["params"]["args"])[:300])
                elif method == "Network.requestWillBeSent":
                    req_urls[m["params"]["requestId"]] = m["params"]["request"].get("url", "")
                elif method == "Network.responseReceived":
                    resp = m["params"]["response"]
                    u = resp.get("url", "")
                    if resp.get("status", 0) >= 400 and not _ignorar_url(u):
                        http_errores.append(f"HTTP {resp['status']} {u[:200]}")
                elif method == "Network.loadingFailed":
                    u = req_urls.get(m["params"].get("requestId", ""), "")
                    if not m["params"].get("canceled") and not _ignorar_url(u):
                        http_errores.append(f"{m['params'].get('errorText', 'failed')} {u[:200]}".strip())
                elif m.get("id") == mio:
                    return m.get("result", {})

        async def js(expr):
            r = await cmd("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True})
            return r.get("result", {}).get("value")

        esquema = "dark" if a.oscuro else "light"
        await cmd("Runtime.enable")
        await cmd("Page.enable")
        await cmd("Network.enable")
        if not a.sin_sonda:
            await cmd("Accessibility.enable")
        await cmd("Emulation.setDeviceMetricsOverride",
                  {"width": ancho, "height": alto, "deviceScaleFactor": 1, "mobile": es_celular})
        await cmd("Emulation.setEmulatedMedia",
                  {"features": [{"name": "prefers-color-scheme", "value": esquema}]})
        await cmd("Page.navigate", {"url": url})
        listo = "document.readyState === 'complete'"
        if a.selector:
            listo += f" && !!document.querySelector({json.dumps(a.selector)})"
        for _ in range(60):
            await asyncio.sleep(0.5)
            if await js(listo):
                break
        await asyncio.sleep(a.espera)

        # clientWidth y no innerWidth: en modo celular el viewport visual se estira hasta el contenido y lo esconde.
        desborde = await js("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        if a.selector:
            caja = await js(f"(() => {{ const e = document.querySelector({json.dumps(a.selector)}); if (!e) return null;"
                            " e.scrollIntoView({block: 'center'}); const r = e.getBoundingClientRect();"
                            " return {x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height, scale: 1}; })()")
        else:
            m = await cmd("Page.getLayoutMetrics")
            t = m["cssContentSize"]
            caja = {"x": 0, "y": 0, "width": ancho, "height": min(t["height"], 16000), "scale": 1}
        if not caja:
            errores.append(f"no está el selector {a.selector}")
        else:
            r = await cmd("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True, "clip": caja})
            Path(salida).parent.mkdir(parents=True, exist_ok=True)
            Path(salida).write_bytes(base64.b64decode(r["data"]))

        sonda = {}
        if not a.sin_sonda:
            dom = await js(f"({JS_SONDA})({json.dumps(es_celular)})") or {}
            ax = await ax_sin_nombre(cmd, await cmd("Accessibility.getFullAXTree"))
            await cmd("Emulation.setEmulatedMedia", {"features": [
                {"name": "prefers-color-scheme", "value": esquema},
                {"name": "prefers-reduced-motion", "value": "reduce"},
            ]})
            await asyncio.sleep(0.2)
            dom_rm = await js(f"({JS_SONDA})({json.dumps(es_celular)})") or {}
            await cmd("Emulation.setEmulatedMedia", {"features": [
                {"name": "prefers-color-scheme", "value": esquema},
                {"name": "prefers-reduced-motion", "value": "no-preference"},
            ]})
            sonda = {
                "http_errores": http_errores,
                "imagenes_rotas": dom.get("imagenes_rotas", []),
                "enlaces_muertos": dom.get("enlaces_muertos", []),
                "controles_tapados": dom.get("controles_tapados", []),
                "targets_chicos": dom.get("targets_chicos", []),
                "ax_sin_nombre": ax,
                "opacidad_cero": dom.get("opacidad_cero", []),
                "opacidad_cero_reducido": dom_rm.get("opacidad_cero", []),
            }

        interacciones = []
        if plan_interacciones and (not es_celular or plan_interacciones.get("en_celular")):
            interacciones = await ejecutar_interacciones(cmd, js, plan_interacciones)

    return errores, desborde, sonda, interacciones


def contar_defectos(errores, desborde, sonda, interacciones):
    n = len(errores) + (1 if desborde and desborde > 0 else 0)
    if sonda:
        for v in sonda.values():
            n += len(v)
    n += sum(1 for r in interacciones if not r["ok"])
    return n


async def principal(a):
    ws_mod = _cargar_websockets()
    exe = navegador()
    plan_interacciones = None
    if a.interacciones:
        p = Path(a.interacciones)
        if not p.is_file():
            raise SystemExit(f"No existe el plan de interacciones: {p}")
        plan_interacciones = json.loads(p.read_text(encoding="utf-8"))

    reporte = {"url": a.url, "vistas": {}, "fallos_total": 0}
    hubo_timeout = False
    for nombre, medida in (("escritorio", a.escritorio), ("celular", a.celular)):
        ancho, alto = map(int, medida.lower().split("x"))
        es_celular = nombre == "celular" or ancho < 700
        perfil = tempfile.mkdtemp()
        # Puerto 0: el navegador elige uno libre y lo anota en el perfil; dos capturas a la vez no chocan.
        proc = subprocess.Popen([exe, "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={perfil}",
                                 "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--hide-scrollbars",
                                 f"--window-size={ancho},{alto}", "about:blank"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            archivo = Path(perfil) / "DevToolsActivePort"
            for _ in range(100):
                if archivo.exists() and archivo.read_text().strip():
                    break
                time.sleep(0.1)
            if not archivo.exists() or not archivo.read_text().strip():
                raise TimeoutError("El navegador no abrió el puerto DevTools a tiempo.")
            puerto = archivo.read_text().split()[0]
            from urllib.request import urlopen
            pestanas = json.load(urlopen(f"http://127.0.0.1:{puerto}/json"))
            ws_url = next(p["webSocketDebuggerUrl"] for p in pestanas if p["type"] == "page")
            salida = f"{a.prefijo}-{nombre}.png"
            # Un bucle de animación puede colgar la captura: el límite mata el navegador igual.
            errores, desborde, sonda, interacciones = await asyncio.wait_for(
                capturar(ws_mod, ws_url, a.url, salida, ancho, alto, a, es_celular, plan_interacciones), a.limite
            )
            defectos = contar_defectos(errores, desborde, sonda, interacciones)
            reporte["fallos_total"] += defectos
            reporte["vistas"][nombre] = {
                "archivo": salida, "ancho": ancho, "alto": alto,
                "desborde_px": desborde, "errores_consola": errores,
                "sonda": sonda, "interacciones": interacciones, "defectos": defectos,
            }
            print(f"{nombre} {ancho}x{alto}: {salida}")
            print(f"  desborde horizontal: {'no' if desborde <= 0 else f'SÍ, {desborde} px'}")
            print(f"  errores de consola: {len(errores) or 'ninguno'}")
            for e in errores:
                print(f"    - {e}")
            if sonda:
                for clave, items in sonda.items():
                    if items:
                        print(f"  {clave}: {len(items)}")
                        for item in items[:5]:
                            print(f"    - {item}")
                if not any(sonda.values()):
                    print("  sonda AAA: sin defectos")
            if interacciones:
                ok_n = sum(1 for r in interacciones if r["ok"])
                print(f"  interacciones: {ok_n}/{len(interacciones)} en verde")
                for r in interacciones:
                    estado = "OK" if r["ok"] else f"FALLÓ ({r['detalle']})"
                    print(f"    - {r['paso']}: {estado}")
        except (asyncio.TimeoutError, TimeoutError):
            hubo_timeout = True
            print(f"{nombre}: se pasó de {a.limite} s; navegador cerrado")
        finally:
            proc.kill()
            shutil.rmtree(perfil, ignore_errors=True)

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(reporte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fallo_interaccion = any(not r["ok"] for v in reporte["vistas"].values() for r in v.get("interacciones", []))
    if hubo_timeout or fallo_interaccion or (a.estricto and reporte["fallos_total"] > 0):
        sys.exit(1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("url")
    p.add_argument("prefijo")
    p.add_argument("--selector")
    p.add_argument("--espera", type=float, default=3)
    p.add_argument("--oscuro", action="store_true")
    p.add_argument("--escritorio", default="1440x900")
    p.add_argument("--celular", default="390x844")
    p.add_argument("--limite", type=float, default=90)
    p.add_argument("--sin-sonda", action="store_true", help="omite la sonda DOM/AXTree/red/reduced-motion")
    p.add_argument("--interacciones", help="ruta a plan JSON con pasos interactivos a probar")
    p.add_argument("--json", help="guarda el reporte estructurado en esta ruta")
    p.add_argument("--estricto", action="store_true", help="sale con código 1 si detecta errores o defectos de sonda")
    asyncio.run(principal(p.parse_args()))
