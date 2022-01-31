from typing import Protocol, runtime_checkable


@runtime_checkable
class Messenger(Protocol):
    def setup(self):
        ...
