from typing import Dict, Callable, Any

class ToolRouter:
    def __init__(self, registry: Dict[str, Callable[..., Any]] | None = None):
        self.registry = registry or {}

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        if not callable(fn):
            raise TypeError("Tool must be callable")
        self.registry[name] = fn

    def available(self) -> list[str]:
        return sorted(self.registry.keys())

    def route(self, name: str, **kwargs) -> Any:
        if name not in self.registry:
            raise KeyError(f"Tool '{name}' not registered")
        return self.registry[name](**kwargs)
