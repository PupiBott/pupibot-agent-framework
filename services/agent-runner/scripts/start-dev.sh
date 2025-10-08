#!/usr/bin/env bash
set -euo pipefail

# Activar virtualenv si existe
if [ -f "$(pwd)/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

# Asegura que la carpeta agent-runner esté en PYTHONPATH para resolver `src.*`
export PYTHONPATH="$(pwd)/services/agent-runner:${PYTHONPATH:-}"

# Puerto configurable
PORT="${PORT:-8000}"

# Arranca uvicorn resolviendo src como paquete raíz del backend
uvicorn src.main:app --host 127.0.0.1 --port "${PORT}" --reload