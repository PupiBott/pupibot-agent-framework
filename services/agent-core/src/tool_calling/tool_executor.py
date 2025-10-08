from dataclasses import dataclass
from typing import Any, Dict
from tool_calling.tool_router import ToolRouter

@dataclass
class ToolCallRequest:
    name: str
    args: Dict[str, Any]

@dataclass
class ToolCallResult:
    name: str
    ok: bool
    output: Any = None
    error: str | None = None

class ToolExecutor:
    def __init__(self, router: ToolRouter | None = None):
        self.router = router or ToolRouter()

    def execute(self, req: ToolCallRequest) -> ToolCallResult:
        try:
            output = self.router.route(req.name, **(req.args or {}))
            return ToolCallResult(name=req.name, ok=True, output=output)
        except Exception as e:
            return ToolCallResult(name=req.name, ok=False, error=str(e))
