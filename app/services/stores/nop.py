from kink import inject

from .. import interfaces


@inject(alias=interfaces.Store)
class NopStore:
    """
    A "Not Operational" store. This store provides no default functionality.
    """

    @staticmethod
    def _needs_factory() -> bool:
        return False
