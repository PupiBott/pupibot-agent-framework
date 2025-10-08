import os, sys, pathlib

# Asegurar que el root del repo esté en sys.path
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importar desde el paquete services/agent-core/src (que ahora es paquete)
from services.agent_core.src.tool_calling.tool_router import ToolRouter
from services.agent_core.src.tool_calling.tool_executor import ToolExecutor, ToolCallRequest

def test_router_register_and_list():
    r = ToolRouter()
    r.register("echo", lambda text: text)
    assert "echo" in r.available()

def test_router_route_success():
    r = ToolRouter()
    r.register("add", lambda a, b: a + b)
    assert r.route("add", a=1, b=2) == 3

def test_router_route_missing():
    r = ToolRouter()
    try:
        r.route("missing")
        assert False, "expected KeyError"
    except KeyError:
        assert True

def test_executor_success_and_error():
    r = ToolRouter()
    r.register("upper", lambda s: s.upper())
    ex = ToolExecutor(router=r)
    ok = ex.execute(ToolCallRequest(name="upper", args={"s": "hi"}))
    assert ok.ok and ok.output == "HI"

    bad = ex.execute(ToolCallRequest(name="missing", args={}))
    assert not bad.ok and isinstance(bad.error, str)
