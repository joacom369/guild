import type { JsonValue } from "@grok/agent-sdk";

export const CLAVE_BUZON = "buzon/propuestas";
export const TOPE = 100;

export type Clase = "comun" | "puntual" | "resultado";

export type Propuesta = {
  fecha: string;
  clase: Clase;
  titulo: string;
  porque: string;
  evidencia: string;
  area: string;
  estado: "nueva";
};

type Kv = {
  get(key: string): Promise<JsonValue | undefined>;
  put(key: string, value: JsonValue): Promise<void>;
};

export function normalizar(texto: string): string {
  return texto
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}

function esPropuesta(valor: JsonValue): valor is Propuesta {
  if (valor === null || typeof valor !== "object" || Array.isArray(valor)) return false;
  const fila = valor as Record<string, JsonValue>;
  return (
    typeof fila.titulo === "string" &&
    typeof fila.clase === "string" &&
    typeof fila.porque === "string" &&
    fila.estado === "nueva"
  );
}

export async function leerPropuestas(kv: Kv): Promise<Propuesta[]> {
  const guardado = await kv.get(CLAVE_BUZON);
  if (!Array.isArray(guardado)) return [];
  return guardado.filter(esPropuesta);
}

export async function registrar(
  kv: Kv,
  entrada: Omit<Propuesta, "fecha" | "estado"> & { fecha?: string },
): Promise<{ agregada: boolean; motivo: string; total: number }> {
  const actuales = await leerPropuestas(kv);
  const clave = normalizar(entrada.titulo);
  if (!clave) return { agregada: false, motivo: "titulo vacio", total: actuales.length };
  if (actuales.some((fila) => normalizar(fila.titulo) === clave)) {
    return { agregada: false, motivo: "ya estaba", total: actuales.length };
  }
  if (actuales.length >= TOPE) {
    return { agregada: false, motivo: "buzon lleno", total: actuales.length };
  }
  const propuesta: Propuesta = {
    fecha: entrada.fecha ?? new Date().toISOString().slice(0, 10),
    clase: entrada.clase,
    titulo: entrada.titulo.trim(),
    porque: entrada.porque.trim(),
    evidencia: entrada.evidencia.trim(),
    area: entrada.area.trim() || entrada.clase,
    estado: "nueva",
  };
  await kv.put(CLAVE_BUZON, [...actuales, propuesta]);
  return { agregada: true, motivo: "nueva", total: actuales.length + 1 };
}
