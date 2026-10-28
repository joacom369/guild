import { defineTool } from "@grok/agent-sdk/tools";
import * as z from "zod/v4";
import { leerPropuestas } from "../lib/buzon.js";

export default defineTool({
  description: "Lista las propuestas de mejora guardadas. No cambia nada.",
  effect: "read",
  inputSchema: z.object({}),
  async execute(_input, ctx) {
    const propuestas = await leerPropuestas(ctx.host.kv);
    return {
      total: propuestas.length,
      propuestas: propuestas.slice(-20),
    };
  },
});
