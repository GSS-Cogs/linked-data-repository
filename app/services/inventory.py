from .messager.drivers import NopMessager
from .store.drivers import NopStore

INVENTORY = {"store": {"Nop": NopStore}, "messager": {"Nop": NopMessager}}
