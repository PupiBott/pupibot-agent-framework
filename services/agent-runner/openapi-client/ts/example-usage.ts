import { Configuration, DefaultApi } from "./index";

const config = new Configuration({ basePath: "http://127.0.0.1:8000" });
const api = new DefaultApi(config);

async function runExample() {
  try {
    // Método detectado para crear
    const createResp = await api.createOperationOperationsPost({ action: "example_action", payload: "hello" } as any);
    console.log("create ->", JSON.stringify(createResp, null, 2));
    // Método detectado para ejecutar/run
    const runResp = await api.executeActionV1AgentExecutePost({ operation_id: String((createResp as any)?.id ?? 12345) } as any);
    console.log("run ->", JSON.stringify(runResp, null, 2));
  } catch (e) {
    console.error("example error:", e);
    process.exit(1);
  }
}

runExample();
