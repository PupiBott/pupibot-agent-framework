import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_post_operations(client):
    response = client.post("/operations", json={"action": "generate_doc", "payload": "test"}, headers={"Authorization": "Bearer static_token"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "pending"

def test_get_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "agent-runner"}

def test_post_operations_run(client, httpx_mock):
    # Mock the document-service response
    httpx_mock.add_response(
        method="POST",
        url="http://document-service:8081/generate",
        json={"status": "ok", "service": "document-service", "document": "contenido"},
    )

    # Create an operation
    create_response = client.post("/operations", json={"action": "generate_doc", "payload": "test"}, headers={"Authorization": "Bearer static_token"})
    assert create_response.status_code == 200
    operation_id = create_response.json()["id"]

    # Run the operation
    run_response = client.post(f"/operations/{operation_id}/run", headers={"Authorization": "Bearer static_token"})
    assert run_response.status_code == 200
    run_data = run_response.json()
    assert run_data["id"] == operation_id
    assert run_data["status"] == "done"
    assert run_data["result"] == {"status": "ok", "service": "document-service", "document": "contenido"}