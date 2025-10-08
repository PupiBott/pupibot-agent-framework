#!/usr/bin/env python3
import json
import sys
import traceback
from pathlib import Path

# Garantiza que el paquete src sea importable desde este script
ROOT = Path(__file__).resolve().parents[2]  # apunta a /services
sys.path.insert(0, str(ROOT / "agent-runner"))  # inserta services/agent-runner en sys.path

try:
    # importa la app FastAPI desde src.main (confirma que main.py define `app`)
    from src.main import app
except Exception:
    # intenta import alternativo si estructura difiere
    try:
        from services.agent_runner.src.main import app
    except Exception:
        print("ERROR: no se pudo importar 'app' desde src.main", file=sys.stderr)
        raise

OUT_DIR = ROOT / "agent-runner" / "openapi"
OUT_PATH = OUT_DIR / "openapi.json"

def main():
    try:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        spec = app.openapi()
        with OUT_PATH.open("w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        print(f"Wrote OpenAPI JSON to {OUT_PATH}")
        return 0
    except Exception:
        print("Failed to generate OpenAPI JSON", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())