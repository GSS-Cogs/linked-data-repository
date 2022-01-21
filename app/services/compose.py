from .store.base import BaseStore
from .messager.base import BaseMessager
from .inventory import STORES, MESSAGERS


class UnknownDriverError(Exception):
    """
    Raised where we are specifying an unknown driver.
    """

    def __init__(self, label: str, service: str):
        self.msg = f'"{label}" driver not found for service: "{service}"'


def _driver_getter(label: str, inventory: dict, driver_name: str) -> (object):
    """
    Factored out logic for selecting driver based on
    provided label
    """
    driver = inventory.get(label, None)
    if not driver:
        raise UnknownDriverError(label, driver_name)
    return driver()


def store(label: str) -> (BaseStore):
    """
    Using the provided label, instantiate and return the requested store
    service.
    """
    return _driver_getter(label, STORES, "store")


def messager(label: str) -> (BaseMessager):
    """
    Using the provided label, instantiate and return the requested messager
    service.
    """
    return _driver_getter(label, MESSAGERS, "messager")
