from .messager.drivers import NopMessager
from .store.drivers import NopStore

STORES = {"Nop": NopStore}

MESSAGERS = {"Nop": NopMessager}
