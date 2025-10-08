#!/usr/bin/env bash
set -euo pipefail

# Activar virtualenv si existe
if [ -f "$(pwd)/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

# Puerto configurable
PORT="${PORT:-8000}"

# Arranca uvicorn usando --app-dir para que 'src' sea resolvible
uvicorn main:app --app-dir "$(pwd)/services/agent-runner/src" --host 127.0.0.1 --port "${PORT}" --reload