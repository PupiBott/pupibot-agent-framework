import pytest
from fastapi.testclient import TestClient
from src.main import app, get_db_connection
from src.db_init import initialize_database

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    initialize_database()
    yield
    conn = get_db_connection()
    conn.execute("DROP TABLE operations")
    conn.close()

def test_idempotency_key(client):
    payload = {
        "action": "create_document",
        "payload": {},
        "idempotency_key": "test-key"
    }

    response1 = client.post("/v1/agent/execute", json=payload, headers={"Authorization": "Bearer static_token"})
    response2 = client.post("/v1/agent/execute", json=payload, headers={"Authorization": "Bearer static_token"})

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["operation_id"] == response2.json()["operation_id"]

@pytest.mark.asyncio  # Mark the test as an asyncio test
@pytest.mark.httpx_mock
async def test_integration_with_mocks(httpx_mock, client):  # Added `client` as a fixture
    # Mock the external service response
    httpx_mock.add_response(
        method="POST",
        url="http://document-service:8081/generate",
        json={"status": "success"},
        match_content=b'{"payload":"test"}'  # Ensure the body matches exactly
    )

    # Define the payload
    payload = {"action": "test_action", "payload": "test"}  # Ensure payload is a string

    # Create an operation
    create_response = client.post("/operations", json=payload, headers={"Authorization": "Bearer static_token"})
    assert create_response.status_code == 200
    operation_id = create_response.json()["id"]

    # Run the operation
    run_response = client.post(f"/operations/{operation_id}/run", headers={"Authorization": "Bearer static_token"})
    assert run_response.status_code == 200

    # Verify the mock was consumed
    assert len(httpx_mock.get_requests()) == 1, "Expected one request to the mocked endpoint"