import { defineSchedule } from "@grok/agent-sdk/schedules";

// 12:00 UTC es las 09:00 en America/Buenos_Aires.
export default defineSchedule({
  cron: "0 12 * * *",
  markdown: `Es la vuelta diaria de automejora. Seguí la skill automejora.
Listá el buzón, corré el auditor del gremio si está en este host, y registrá sólo propuestas nuevas.
No edites skills ni instrucciones. No mandes mensajes afuera.
Cerrá con la lista de lo nuevo y el total del buzón.`,
});
