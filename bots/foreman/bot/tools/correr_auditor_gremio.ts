import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { defineTool } from "@grok/agent-sdk/tools";
import * as z from "zod/v4";

const execFileAsync = promisify(execFile);
const TOPE_SALIDA = 8000;

function raizGremio(): string | null {
  const aqui = path.dirname(fileURLToPath(import.meta.url));
  const candidatos = [process.env.GUILD_ROOT, path.resolve(aqui, "../../../..")].filter(
    (candidato): candidato is string => Boolean(candidato),
  );
  for (const raiz of candidatos) {
    if (existsSync(path.join(raiz, "foundry/scripts/auditar_gremio.py"))) return raiz;
  }
  return null;
}

export default defineTool({
  description:
    "Corre el auditor del gremio si el repositorio está en este host. Devuelve el reporte. No escribe el buzón ni edita skills.",
  effect: "read",
  inputSchema: z.object({
    dinamico: z.boolean().optional(),
  }),
  async execute({ dinamico }) {
    const raiz = raizGremio();
    if (!raiz) {
      return {
        disponible: false,
        motivo: "El repositorio del gremio no está en este host. La automejora sigue con el buzón del agente.",
      };
    }
    const script = path.join(raiz, "foundry/scripts/auditar_gremio.py");
    const args = [script, ...(dinamico ? ["--dinamico"] : [])];
    try {
      const { stdout, stderr } = await execFileAsync("python3", args, {
        cwd: raiz,
        timeout: 20_000,
        maxBuffer: 1_000_000,
      });
      const salida = `${stdout}${stderr}`.slice(0, TOPE_SALIDA);
      return { disponible: true, ok: true, salida };
    } catch (error) {
      const fallo = error as { stdout?: string; stderr?: string; code?: number; message?: string };
      const salida = `${fallo.stdout ?? ""}${fallo.stderr ?? fallo.message ?? ""}`.slice(0, TOPE_SALIDA);
      return { disponible: true, ok: false, codigo: fallo.code ?? 1, salida };
    }
  },
});
