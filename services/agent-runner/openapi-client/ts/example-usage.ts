import { Configuration, DefaultApi } from "./index";

const config = new Configuration({ basePath: "http://127.0.0.1:8000" });
const api = new DefaultApi(config);

async function runExample() {
  try {
    const createResp = await (api as any).createOperationOperationsPost({ action: "example_action", payload: "hello" } as any);
    console.log("create ->", JSON.stringify(createResp?.data ?? createResp ?? null, null, 2));
    const opId = (createResp?.data && ((createResp.data as any).id)) || (createResp?.id) || 12345;
    const runResp = await (api as any).executeActionV1AgentExecutePost({ operation_id: String(opId) } as any);
    console.log("run ->", JSON.stringify(runResp?.data ?? runResp ?? null, null, 2));
  } catch (err: any) {
    if (err?.response) {
      console.error("Request failed status:", err.response.status, "body:", JSON.stringify(err.response.data || err.response, null, 2));
    } else {
      console.error("Unexpected error:", err?.message ?? err);
    }
    process.exit(1);
  }
}

runExample();
