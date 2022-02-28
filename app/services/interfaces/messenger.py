from typing import Protocol, runtime_checkable

from kink import di


@runtime_checkable
class Messenger(Protocol):
    pass
