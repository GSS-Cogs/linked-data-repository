from kink import inject
from app.services import interfaces


@inject(alias=interfaces.Messenger)
class NopMessenger:
    """
    A "Not Operational" messenger. This messenger provides no default functionality.
    """

    def setup(self):
        pass
