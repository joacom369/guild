import { defineEval } from "@grok/agent-sdk/evals";

export default defineEval({
  tags: ["smoke"],
  description: "Una propuesta de mejora se registra y después se puede listar.",
  async test(t) {
    await t.send(
      'Registrá una propuesta clase comun, titulo "piloto de automejora del gremio", porque "verifica que el buzón durable guarda la propuesta", evidencia "eval smoke", area comun. Después listá las propuestas.',
    );
    t.succeeded();
    t.calledTool("registrar_propuesta");
    t.calledTool("listar_propuestas");
    t.notCalledTool("correr_auditor_gremio");
  },
});
