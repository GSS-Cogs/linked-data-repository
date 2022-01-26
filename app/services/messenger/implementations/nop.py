from app.services.messenger.base import BaseMessenger


class NopMessenger(BaseMessenger):
    """
    A "Not Operational" messenger. This messenger will satisfy the
    abstract but otherwise provides no default functionality.
    """

    def setup(self, *args, **kwargs):
        pass
