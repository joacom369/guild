"""Captura una página en escritorio y celular con Chrome o Edge sin ventana, y reporta errores y desborde.

Uso:
    python foto_pagina.py URL PREFIJO [--selector CSS] [--espera 3] [--oscuro]
                          [--escritorio 1440x900] [--celular 390x844] [--limite 90]

Escribe PREFIJO-escritorio.png y PREFIJO-celular.png (la página entera, o sólo el selector si se pasa).
Necesita `pip install websockets`. Para páginas con 3D, `--espera 9`.
"""
import argparse
import asyncio
import base64
import json
import os
import shutil
import subprocess
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


async def capturar(ws_mod, ws_url, url, salida, ancho, alto, a):
    errores, n = [], 0
    async with ws_mod.connect(ws_url, max_size=2 ** 28) as ws:
        async def cmd(metodo, params=None):
            nonlocal n
            n += 1
            mio = n
            await ws.send(json.dumps({"id": mio, "method": metodo, "params": params or {}}))
            while True:
                m = json.loads(await ws.recv())
                if m.get("method") == "Runtime.exceptionThrown":
                    d = m["params"]["exceptionDetails"]
                    errores.append(d.get("exception", {}).get("description", d.get("text", ""))[:300])
                elif m.get("method") == "Runtime.consoleAPICalled" and m["params"]["type"] == "error":
                    errores.append(" ".join(str(x.get("value", x.get("description", ""))) for x in m["params"]["args"])[:300])
                elif m.get("id") == mio:
                    return m.get("result", {})

        async def js(expr):
            r = await cmd("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True})
            return r.get("result", {}).get("value")

        await cmd("Runtime.enable")
        await cmd("Page.enable")
        await cmd("Emulation.setDeviceMetricsOverride",
                  {"width": ancho, "height": alto, "deviceScaleFactor": 1, "mobile": ancho < 700})
        await cmd("Emulation.setEmulatedMedia",
                  {"features": [{"name": "prefers-color-scheme", "value": "dark" if a.oscuro else "light"}]})
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
            Path(salida).write_bytes(base64.b64decode(r["data"]))
    return errores, desborde


async def principal(a):
    ws_mod = _cargar_websockets()
    exe = navegador()
    for nombre, medida in (("escritorio", a.escritorio), ("celular", a.celular)):
        ancho, alto = map(int, medida.lower().split("x"))
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
            puerto = archivo.read_text().split()[0]
            from urllib.request import urlopen
            pestanas = json.load(urlopen(f"http://127.0.0.1:{puerto}/json"))
            ws_url = next(p["webSocketDebuggerUrl"] for p in pestanas if p["type"] == "page")
            salida = f"{a.prefijo}-{nombre}.png"
            # Un bucle de animación puede colgar la captura: el límite mata el navegador igual.
            errores, desborde = await asyncio.wait_for(capturar(ws_mod, ws_url, a.url, salida, ancho, alto, a), a.limite)
            print(f"{nombre} {ancho}x{alto}: {salida}")
            print(f"  desborde horizontal: {'no' if desborde <= 0 else f'SÍ, {desborde} px'}")
            print(f"  errores de consola: {len(errores) or 'ninguno'}")
            for e in errores:
                print(f"    - {e}")
        except asyncio.TimeoutError:
            print(f"{nombre}: se pasó de {a.limite} s; navegador cerrado")
        finally:
            proc.kill()
            shutil.rmtree(perfil, ignore_errors=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("url")
    p.add_argument("prefijo")
    p.add_argument("--selector")
    p.add_argument("--espera", type=float, default=3)
    p.add_argument("--oscuro", action="store_true")
    p.add_argument("--escritorio", default="1440x900")
    p.add_argument("--celular", default="390x844")
    p.add_argument("--limite", type=float, default=90)
    asyncio.run(principal(p.parse_args()))
