from typing import Protocol, runtime_checkable


@runtime_checkable
class Messenger(Protocol):

    @staticmethod
    def _needs_factory() -> bool:
        ...
