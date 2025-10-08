import { Configuration, DefaultApi } from "./index";
const config = new Configuration({ basePath: "http://127.0.0.1:8000" });
const api = new DefaultApi(config);
async function runExample() {
  try {
    // La API espera un objeto con action y payload, ajustamos la llamada para ser robustos.
    const createResp = await api.createOperation({ action: "example_action", payload: "hello" } as any);
    // El ID real de la respuesta estará dentro de la data
    const opId = (createResp.data as any)?.id; 
    console.log("createOperation ->", JSON.stringify(createResp.data, null, 2));

    if (opId) {
      const runResp = await api.runOperation({ operation_id: String(opId) } as any);
      console.log("runOperation ->", JSON.stringify(runResp.data, null, 2));
    } else {
      console.error("Error: ID de operación no encontrado en la respuesta.");
      process.exit(1);
    }
  } catch (e) {
    console.error("example error:", e.response?.data || e.message);
    process.exit(1);
  }
}
runExample();
