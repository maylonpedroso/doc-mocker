__all__ = ["FunctionBindDescriptor"]

from typing import Callable, Any, Type


class FunctionBindDescriptor:
    def __init__(self, name: str, method: Callable, reverse: Callable = None) -> None:
        self._name = name
        self._method = method
        self._reverse = reverse

    def __get__(self, instance: Any, owner: Type) -> Any:
        return self._method(getattr(instance, self._name))

    def __set__(self, instance: Any, value: Any) -> None:
        if callable(self._reverse):
            setattr(instance, self._name, self._reverse(value))
        else:
            raise AttributeError(
                "Must provide a reverse method to be able to assign a value"
            )
