import pytest
respx = pytest.importorskip("respx")
import httpx
from fastapi.testclient import TestClient
from src.main import app

@respx.mock
def test_external_call_with_respx():
    route = respx.post("http://document-service:8081/generate").mock(
        return_value=httpx.Response(200, json={"document": "ok"})
    )

    with TestClient(app) as client:
        create = client.post(
            "/operations",
            json={"action": "generate_doc", "payload": "test", "idempotency_key": "respx"},
        )
        assert create.status_code == 200
        opid = create.json()["id"]

        run = client.post(f"/operations/{opid}/run")
        assert run.status_code == 200
        assert route.called