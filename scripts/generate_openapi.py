import json
import pathlib

from services.agent_runner.src.main import app

current_spec = app.openapi()
pathlib.Path("openapi.current.json").write_text(
    json.dumps(current_spec, indent=2), encoding="utf-8"
)
