import inspect
from typing import Union

from .store.base import BaseStore
from .messager.base import BaseMessager
from .inventory import INVENTORY


class UnknownDriverError(Exception):
    """
    Raised where we are specifying an unknown driver.
    """

    def __init__(self, label: str, service: str):
        self.msg = f'"{label}" driver not found for service: "{service}"'


class Composer:
    """
    For selecting and (where necessary) instantiating type checked service drivers
    """

    def __init__(self, config, enforce_base_classes: bool):
        self.inventory = INVENTORY
        self.config = config
        self.enforce_base_classes = enforce_base_classes

    def _driver_from_label(self, label: str, driver_name: str) -> (object):
        """
        Select a known driver based on the str label passed in
        """
        driver = self.inventory[driver_name].get(label, None)
        if not driver:
            raise UnknownDriverError(label, driver_name)
        return driver

    def _use_driver(self, driver: object, driver_base_class: object) -> (object):
        """
        Instantiates and configures driver (where needed) and validates it complies with
        the expected Base class before returning it.
        """

        # Instanitate and configure where needed
        if inspect.isclass(driver):
            driver = driver()
            driver.setup(config=self.config)

        # Confirm driver is extending the correct parent class
        if self.enforce_base_classes:
            driver_in_use_base = driver.__class__.__bases__[-1]
            if str(driver_in_use_base) != str(driver_base_class):
                raise TypeError(
                    f"Driver '{driver_in_use_base}' does not but should have parent class '{driver_base_class}'."
                )

        return driver

    def store(self, driver: Union[str, object]) -> (BaseStore):
        """
        Applies sanity checks and setup functions then return the requested store driver.
        """
        if isinstance(driver, str):
            driver = self._driver_from_label(driver, "store")
        return self._use_driver(driver, BaseStore)

    def messager(self, driver: Union[str, object]) -> (BaseMessager):
        """
        Applies sanity checks and setup functions then return the requested messager driver.
        """
        if isinstance(driver, str):
            driver = self._driver_from_label(driver, "messager")
        return self._use_driver(driver, BaseMessager)
