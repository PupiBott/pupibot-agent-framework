import importlib.util
import sys
from pathlib import Path
import pytest

# --- Solución de Carga Dinámica para evitar problemas de PYTHONPATH ---
# Cargar dinámicamente call_executor.py desde services/agent-core/src
# Esto es necesario porque 'agent-core' no es un paquete válido por el guion.
module_path = Path(__file__).resolve().parents[1] / "src" / "call_executor.py"
spec = importlib.util.spec_from_file_location("agent_core.call_executor", str(module_path))
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

# El módulo cargado dinámicamente es 'mod'
call_agent_runner_api = mod.call_agent_runner_api


def test_call_executor_smoke(monkeypatch):
    """
    Verifica que el executor pueda hacer un POST y procesar un resultado 200 OK
    usando un mock (parcheando requests.Session.post).
    """
    class MockResp:
        def __init__(self):
            self.status_code = 200
            self.text = '{"id": 3}' # Simula respuesta JSON
            
        def raise_for_status(self): 
            pass # 200 OK

        def json(self):
            return {"id": 3, "status": "pending"}

    # Función que se ejecuta en lugar de la llamada HTTP real
    def mock_post(*args, **kwargs):
        return MockResp()

    # parchear requests.Session.post en el módulo cargado
    import requests
    monkeypatch.setattr(requests.Session, "post", lambda self, *a, **k: mock_post())
    
    # Assert
    assert call_agent_runner_api("http://127.0.0.1:8000", "createOperationOperationsPost", {"action":"x","payload":"y"}) == {"id": 3, "status": "pending"}

# Para la prueba, también probamos una función no implementada
def test_call_executor_unimplemented():
    result = call_agent_runner_api("http://127.0.0.1:8000", "someRandomFunction", {})
    assert "Función no implementada" in result["error"]
