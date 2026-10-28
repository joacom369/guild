import { defineTool } from "@grok/agent-sdk/tools";
import * as z from "zod/v4";
import { registrar } from "../lib/buzon.js";

export default defineTool({
  description:
    "Guarda una propuesta de mejora en el buzón durable. La misma propuesta dos veces no se duplica. No edita skills ni instrucciones.",
  effect: "idempotent",
  inputSchema: z.object({
    clase: z.enum(["comun", "puntual", "resultado"]),
    titulo: z.string().min(8).max(200),
    porque: z.string().min(8).max(500),
    evidencia: z.string().min(1).max(500),
    area: z.string().min(1).max(80),
  }),
  async execute(input, ctx) {
    const resultado = await registrar(ctx.host.kv, input);
    return resultado;
  },
});
