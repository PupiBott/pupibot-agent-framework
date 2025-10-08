import pytest
from services.agent_core.src.call_executor import call_agent_runner_api

# Este test verifica que nuestro executor envíe la solicitud POST y maneje la respuesta 200 OK
def test_call_executor_create_operation_smoke(monkeypatch):
    """Mockea la llamada POST para asegurar que call_executor se comporta correctamente."""
    
    # Clase Mock que simula la respuesta de requests
    class MockResp:
        def __init__(self): 
            self.status_code = 200
            self.text = '{"id": 3}'

        def raise_for_status(self): 
            # No hace nada para simular un 200 OK
            pass 

        def json(self): 
            return {"id": 3, "status": "pending"}

    # Función Mock que será inyectada en requests.Session.post
    def mock_post(*args, **kwargs): 
        assert "X-Request-Id" in kwargs.get('headers', {}) # Asegura que el Request ID está presente
        assert kwargs.get('json', {}).get('action') == "x" # Asegura que el payload se pasa
        return MockResp()

    import requests
    # Usamos monkeypatch para reemplazar el método 'post' de la requests.Session
    monkeypatch.setattr(requests.Session, 'post', lambda self, *a, **k: mock_post(*a, **k))

    # Llamamos a la función que queremos probar
    result = call_agent_runner_api("http://127.0.0.1:8000", "createOperationOperationsPost", {"action":"x","payload":"y"})
    
    # Verificamos el resultado esperado
    assert result == {"id": 3, "status": "pending"}

# También necesitamos añadir los tests de excepción (ej: 404/500), pero por ahora, el smoke es suficiente.
