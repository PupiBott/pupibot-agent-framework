#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

WF=".github/workflows/agent-core-ci.yml"

# 1) Asegurar carpeta
mkdir -p "$(dirname "$WF")"

# 2) Verificar que el archivo existe y contiene el workflow mínimo; si no existe, crear el workflow limpio
if [ ! -f "$WF" ] || ! grep -q "name: agent-core-ci" "$WF"; then
  cat > "$WF" <<'YML'
name: agent-core-ci

on:
  workflow_dispatch:
  pull_request:
    paths:
      - 'services/**'
      - 'requirements-dev.txt'
      - '.github/workflows/agent-core-ci.yml'
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest
    env:
      PYTHONPATH: ${{ github.workspace }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dev dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-dev.txt
      - name: Debug env before tests
        run: |
          echo "PYTHONPATH=$PYTHONPATH"
          python -V
          which python
          python -m pip show pytest || true
          python -c "import sys; print('sys.path[0:6]=', sys.path[:6])"
      - name: Run unit tests
        run: python -m pytest -q services/agent_core/tests

  integration:
    needs: validate
    runs-on: ubuntu-latest
    env:
      PYTHONPATH: ${{ github.workspace }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dev dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-dev.txt
      - name: Run integration tests
        run: |
          echo "Running integration tests for agent_runner"
          python -c "import sys; print('PYTHONPATH=', sys.path[0])"
          python -m pytest -q services/agent_runner/tests

  contract_check:
    needs: [validate, integration]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dev dependencies
        run: python -m pip install -r requirements-dev.txt
      - name: Generate current OpenAPI spec
        run: |
          python - <<'PY'
from services.agent_runner.src.main import app
import json, pathlib
current_spec = app.openapi()
pathlib.Path("openapi.current.json").write_text(
    json.dumps(current_spec, indent=2), encoding="utf-8"
)
PY
      - name: Check for contract changes
        run: |
          diff openapi.snapshot.json openapi.current.json
      - name: Contract Check Passed
        if: success()
        run: echo "✅ OpenAPI contract matches snapshot."
YML
  echo "Created workflow at $WF"
fi

# 3) Lint YAML if yq is available (non-fatal)
if command -v yq >/dev/null 2>&1; then
  echo "Validando sintaxis YAML con yq..."
  yq e . "$WF" >/dev/null
else
  echo "yq no está instalado; omitiendo validación YAML local."
fi

# 4) Hacer commit trivial para forzar ejecución por push
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
STAMP_FILE=".ci/last_workflow_trigger"
mkdir -p "$(dirname "$STAMP_FILE")"
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$STAMP_FILE"
git add "$WF" "$STAMP_FILE"

# Only commit if there are staged changes
if ! git diff --cached --quiet; then
  git commit -m "ci: ensure workflow_dispatch and trigger CI run (stamp)"
  git push origin "$BRANCH"
  echo "Push realizado a rama $BRANCH. Esto disparará el workflow por evento push."
else
  echo "No hay cambios para commitear; igual intentaremos forzar ejecución manual."
fi

# 5) Intentar ejecutar manualmente si gh CLI y workflow registered
if command -v gh >/dev/null 2>&1; then
  echo "Intentando ejecutar workflow manualmente con gh workflow run..."
  # obtener el nombre del workflow file en remoto
  gh workflow run agent-core-ci.yml || {
    echo "gh workflow run falló o el workflow no está aún registrado. El push debería activar el workflow."
  }
else
  echo "gh CLI no disponible; confía en el push para activar el workflow."
fi

echo "Listo. Revisa Actions en GitHub para confirmar la ejecución."