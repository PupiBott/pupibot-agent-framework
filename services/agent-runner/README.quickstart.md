Quickstart for UI integration

1. Start backend locally:
   TESTING=1 python -m uvicorn services.agent-runner.src.main:app --host 127.0.0.1 --port 8000

2. From the TS client folder:
   cd services/agent-runner/openapi-client/ts
   npm ci
   npx ts-node example-usage.ts

3. Endpoints:
   POST /operations -> create operation
   POST /v1/agent/execute -> execute operation (body: action, payload, idempotency_key)
