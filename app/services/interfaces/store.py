from typing import Protocol, runtime_checkable


@runtime_checkable
class Store(Protocol):

    @staticmethod
    def _needs_factory() -> bool:
        ...
