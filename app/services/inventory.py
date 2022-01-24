from .messager.implementations import NopMessager
from .store.implementations import NopStore

INVENTORY = {"store": {"Nop": NopStore}, "messager": {"Nop": NopMessager}}
