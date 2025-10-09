from typing import Any, Callable, Dict, List


class ToolRouter:
    def __init__(self):
        self._registry: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]):
        self._registry[name] = fn

    def get(self, name: str):
        return self._registry.get(name)

    def available(self) -> List[str]:
        """Return list of registered tool names."""
        return list(self._registry.keys())

    def route(self, name: str, /, *args, **kwargs) -> Any:
        """
        Execute the registered tool with given args/kwargs.
        Raise KeyError if tool not found.
        """
        fn = self.get(name)
        if fn is None:
            raise KeyError(f"tool not found: {name}")
        return fn(*args, **kwargs)
