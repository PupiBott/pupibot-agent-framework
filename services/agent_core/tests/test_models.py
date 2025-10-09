from pydantic import ValidationError
from services.agent_core.src.tool_calling.models import ToolCallRequest

def test_toolcallrequest_requires_name():
    try:
        ToolCallRequest.model_validate({"args": {}})
        assert False, "expected ValidationError"
    except ValidationError:
        assert True
