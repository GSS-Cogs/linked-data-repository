from kink import inject, di

from .. import interfaces


@inject(alias=interfaces.Store)
class NopStore:
    """
    A "Not Operational" store. This store provides no default functionality.
    """
    
    ...
