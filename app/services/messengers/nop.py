from kink import inject

from .. import interfaces


@inject(alias=interfaces.Messenger)
class NopMessenger:
    """
    A "Not Operational" messenger. This messenger provides no default functionality.
    """

    @staticmethod
    def _needs_factory() -> bool:
        return False
