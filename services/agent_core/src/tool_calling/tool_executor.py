from typing import Any

from .models import ToolCallRequest, ToolCallResult
from .tool_router import ToolRouter


class ToolExecutor:
    def __init__(self, router: ToolRouter):
        self.router = router

    def execute(self, req: ToolCallRequest) -> ToolCallResult:
        fn = self.router.get(req.name)
        if not fn:
            return ToolCallResult(ok=False, error=f"tool not found: {req.name}")
        try:
            # call with args dict expanded if callable supports kwargs
            result = fn(**req.args) if isinstance(req.args, dict) else fn(req.args)
            return ToolCallResult(ok=True, output=result)
        except Exception as e:
            return ToolCallResult(ok=False, error=str(e))
