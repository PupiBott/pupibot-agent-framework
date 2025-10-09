from fastapi import APIRouter

from services.agent_core.src.tool_calling.models import (ToolCallRequest,
                                                         ToolCallResult)
from services.agent_core.src.tool_calling.tool_executor import ToolExecutor
from services.agent_core.src.tool_calling.tool_router import ToolRouter

router = APIRouter(prefix="/tools", tags=["tools"])

# Minimal router and executor for tests
_router = ToolRouter()
_router.register("echo", lambda text: text)
_executor = ToolExecutor(router=_router)


@router.post("/execute", response_model=ToolCallResult)
async def execute_tool(req: ToolCallRequest) -> ToolCallResult:
    return _executor.execute(req)
