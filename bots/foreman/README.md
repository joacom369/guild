# foreman

Piloto del capataz. Propone mejoras del gremio y las guarda en un buzón durable. No edita skills.

La rutina `automejora` está escrita para las 09:00 de Buenos Aires (12:00 UTC). No corre hasta que el agente esté desplegado. En `--dev` las rutinas no se disparan solas.

```bash
npx --yes @grok/agent-sdk@0.4.0 validate --dir bots/foreman
npx --yes @grok/agent-sdk@0.4.0 tool call registrar_propuesta --dir bots/foreman --input '{"clase":"comun","titulo":"piloto de automejora del gremio","porque":"verifica el buzon","evidencia":"readme","area":"comun"}'
npx --yes @grok/agent-sdk@0.4.0 dev bots/foreman
```

El despliegue a Cursor pide `CURSOR_SERVICE_ACCOUNT_KEY`. Sin esa cuenta este piloto queda en el repositorio y no queda prendido.
