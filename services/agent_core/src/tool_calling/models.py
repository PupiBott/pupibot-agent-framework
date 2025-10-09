from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class ToolCallRequest(BaseModel):
    name: str = Field(..., description="Tool name")
    args: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")

class ToolCallResult(BaseModel):
    ok: bool
    output: Optional[Any] = None
    error: Optional[str] = None
