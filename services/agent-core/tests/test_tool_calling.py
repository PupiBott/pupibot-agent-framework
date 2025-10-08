import importlib.util, pathlib, sys

# Permite importar módulos sin paquete formal
SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
spec = importlib.util.spec_from_file_location("tool_router", SRC / "tool_calling" / "tool_router.py")
tool_router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool_router)

spec2 = importlib.util.spec_from_file_location("tool_executor", SRC / "tool_calling" / "tool_executor.py")
tool_executor = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(tool_executor)

def test_router_register_and_list():
    r = tool_router.ToolRouter()
    r.register("echo", lambda text: text)
    assert "echo" in r.available()

def test_router_route_success():
    r = tool_router.ToolRouter()
    r.register("add", lambda a, b: a + b)
    assert r.route("add", a=1, b=2) == 3

def test_router_route_missing():
    r = tool_router.ToolRouter()
    try:
        r.route("missing")
        assert False, "expected KeyError"
    except KeyError:
        assert True

def test_executor_success_and_error():
    r = tool_router.ToolRouter()
    r.register("upper", lambda s: s.upper())
    ex = tool_executor.ToolExecutor(router=r)
    ok = ex.execute(tool_executor.ToolCallRequest(name="upper", args={"s": "hi"}))
    assert ok.ok and ok.output == "HI"

    bad = ex.execute(tool_executor.ToolCallRequest(name="missing", args={}))
    assert not bad.ok and isinstance(bad.error, str)
