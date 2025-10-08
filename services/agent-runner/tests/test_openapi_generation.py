from src.main import app

def test_openapi_contains_operations():
    spec = app.openapi()
    paths = spec.get("paths", {})
    assert "/operations" in paths
    assert "/operations/{operation_id}/run" in paths or any(
        "/operations/" in p and "/run" in p for p in paths
    )