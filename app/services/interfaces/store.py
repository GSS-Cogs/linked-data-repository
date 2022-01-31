from typing import Protocol, runtime_checkable


@runtime_checkable
class Store(Protocol):
    def setup(self):
        ...
