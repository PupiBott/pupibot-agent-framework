import pytest
from httpx import ASGITransport, AsyncClient

from services.agent_runner.src.main import app


@pytest.mark.asyncio
async def test_execute_tool_echo():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/tools/execute", json={"name": "echo", "args": {"text": "hola"}}
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["output"] == "hola"


@pytest.mark.asyncio
async def test_execute_tool_missing():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/tools/execute", json={"name": "noexiste", "args": {}})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is False
    assert "error" in data
