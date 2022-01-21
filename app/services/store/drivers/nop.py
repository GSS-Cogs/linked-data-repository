from app.services.store.base import BaseStore

class NopStore(BaseStore):
    """
    A "Not Operational" store. This store needs to satisfy the
    abstract but otherwise provide no default functionality.
    """

    def setup(self, *args, **kwargs):
        pass
