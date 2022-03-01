from kink import inject, di

from .. import interfaces


@inject(alias=interfaces.Messenger)
class NopMessenger:
    """
    A "Not Operational" messenger. This messenger provides no default functionality.
    """

    ...
