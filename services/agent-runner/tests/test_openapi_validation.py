import json

from src.main import app


def test_openapi_has_required_paths_and_schemas():
    spec = app.openapi()
    paths = spec.get("paths", {})
    assert "/operations" in paths
    assert "/operations/{id}" in paths or any(
        p.startswith("/operations/") for p in paths
    )
    assert any(
        p.endswith("/run") for p in paths if p.startswith("/operations/")
    ), "Missing /operations/{id}/run path"

    schemas = spec.get("components", {}).get("schemas", {})
    assert (
        "Operation" in schemas or "operation" in schemas
    ), "Missing Operation schema in components/schemas"
