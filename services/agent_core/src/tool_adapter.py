import json
from pathlib import Path

from google.genai import types


def load_openapi_tool(path: str) -> types.Tool:
    """Carga el archivo openapi.json y lo transforma en un objeto Tool para Gemini."""
    with open(path, "r") as f:
        spec = json.load(f)
    return types.Tool.from_openapi(spec)
