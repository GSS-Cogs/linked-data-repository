from app.services.messager.base import BaseMessager


class NopMessager(BaseMessager):
    """
    A "Not Operational" messager. This messager will satisfy the
    abstract but otherwise provides no default functionality.
    """

    def setup(self, *args, **kwargs):
        pass
