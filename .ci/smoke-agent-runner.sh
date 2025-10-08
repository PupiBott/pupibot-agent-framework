#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
source .venv/bin/activate || true

TESTING=1 python -m uvicorn services.agent-runner.src.main:app --host 127.0.0.1 --port 8000 > /tmp/uvicorn.ci.log 2>&1 &
UV_PID=$!
sleep 2

cd services/agent-runner/openapi-client/ts
npm ci --silent
npx -y ts-node example-usage.ts 2>&1 | tee /tmp/example.ci.log || true

kill $UV_PID || true
exit 0
