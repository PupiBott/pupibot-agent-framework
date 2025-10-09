import json

import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock
from src.db_init import initialize_database
from src.main import app, get_db_connection


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
        "idempotency_key": "test-key",
    }

    response1 = client.post(
        "/v1/agent/execute",
        json=payload,
        headers={"Authorization": "Bearer static_token"},
    )
    response2 = client.post(
        "/v1/agent/execute",
        json=payload,
        headers={"Authorization": "Bearer static_token"},
    )

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["operation_id"] == response2.json()["operation_id"]


@pytest.mark.asyncio  # Mark the test as an asyncio test
@pytest.mark.httpx_mock
async def test_integration_with_mocks(
    httpx_mock: HTTPXMock, client
):  # Added `client` as a fixture
    # Define the expected payload
    expected_body = json.dumps({"payload": "test"}).encode("utf-8")

    # Mock flexible: consume by URL+method, without strict match_content
    httpx_mock.add_response(
        method="POST",
        url="http://document-service:8081/generate",
        json={"document": "ok"},
        status_code=200,
    )

    # Create operation with explicit preconditions
    payload = {"action": "generate_doc", "payload": "test"}
    create = client.post(
        "/operations", json=payload, headers={"Authorization": "Bearer static_token"}
    )
    assert create.status_code == 200
    data = create.json()
    operation_id = data["id"]

    # Execute operation
    run = client.post(
        f"/operations/{operation_id}/run",
        headers={"Authorization": "Bearer static_token"},
    )
    assert run.status_code == 200

    # Validate mock consumption and sent payload
    requests = httpx_mock.get_requests()
    sent = [
        r
        for r in requests
        if str(r.url) == "http://document-service:8081/generate" and r.method == "POST"
    ]
    assert sent, "External POST to /generate was not performed"
    assert json.loads(sent[-1].content)["payload"] == "test"
