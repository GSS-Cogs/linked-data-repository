import inspect
from typing import Union

from .store.base import BaseStore
from .messager.base import BaseMessager
from .inventory import INVENTORY


class UnknownImplementationError(Exception):
    """
    Raised where we are specifying an unknown implementation.
    """

    def __init__(self, label: str, service: str):
        self.msg = f'Implementation "{label}" not found for service: "{service}"'


class Composer:
    """
    For selecting and (where necessary) instantiating type checked service implementations
    """

    def __init__(self, config, enforce_base_classes: bool):
        self.inventory = INVENTORY
        self.config = config
        self.enforce_base_classes = enforce_base_classes

    def _get_from_label(self, label: str, implementation_name: str) -> (object):
        """
        Select a known implementation based on the str label passed in
        """
        implementation = self.inventory[implementation_name].get(label, None)
        if not implementation:
            raise UnknownImplementationError(label, implementation_name)
        return implementation

    def _use(self, implementation: object, base_class: object) -> (object):
        """
        Instantiates (where needed) and validates a given impementation complies with
        the expected Base class before returning it.
        """

        # Instanitate and configure
        # note: this is the expected behaviour, we're accounting for pre-instanitation
        # to allow flexibility for test scenarios.
        if inspect.isclass(implementation):
            implementation = implementation()
            implementation.setup(config=self.config)

        # Confirm implementation is extending the correct base class
        if self.enforce_base_classes:
            implementation_in_use_base = implementation.__class__.__bases__[-1]
            if str(implementation_in_use_base) != str(base_class):
                raise TypeError(
                    f"'{implementation_in_use_base}' does not but should have base class '{base_class}'."
                )

        return implementation

    # -----------------------
    # From here is wrappers, it would be best to continue the pattern as
    # servies are added

    def store(self, implementation: Union[str, object]) -> (BaseStore):
        """
        Applies sanity checks and setup functions then return the requested store implementation.
        """
        if isinstance(implementation, str):
            implementation = self._get_from_label(implementation, "store")
        return self._use(implementation, BaseStore)

    def messager(self, implementation: Union[str, object]) -> (BaseMessager):
        """
        Applies sanity checks and setup functions then return the requested messager implementation.
        """
        if isinstance(implementation, str):
            implementation = self._get_from_label(implementation, "messager")
        return self._use(implementation, BaseMessager)
