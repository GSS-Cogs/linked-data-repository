from kink import inject
from app.services import interfaces


@inject(alias=interfaces.Store)
class NopStore:
    """
    A "Not Operational" store. This store provides no default functionality.
    """

    def setup(self):
        pass
