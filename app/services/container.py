from configparser import ConfigParser
from typing import Type, TypeVar, Union

from kink import di
from sanic import Sanic

from . import interfaces
from .inventory import INVENTORY

T = TypeVar("T")


class UnknownImplementationError(Exception):
    """
    Raised where we are specifying an unknown implementation.
    """

    def __init__(self, label: str, service: str):
        self.msg = f'Implementation "{label}" not found for interface: "{service}"'



class _Specifier:
    """
    di (direct injection containwer) wrapper: allows service instantiation
    from a str name (such as when acquired from the config) and as either a
    singleton or factory.
    """

    def __init__(self, config: ConfigParser, implementations: dict):
        self.config = config
        self.implementations = implementations

    def add_service(
        self,
        interface: Union[Type[T], str, None],
        service_label: str,
        factory=False,
        **kwargs,
    ):
        """
        di (direct injection containwer) wrapper: allows service instantiation
        from a str name (such as when acquired from the config) and as either a
        singleton or factory.
        """

        declaration = self.implementations[service_label]

        # Set default, where None is declared
        if not declaration:
            declaration = self.config[service_label.upper()]["default_implementation"]

        # If str not class, get the class from the inventory
        try:
            if isinstance(declaration, str):
                service = INVENTORY[service_label][declaration]
            else:
                service = declaration
        except KeyError:
            raise UnknownImplementationError(service_label, interface)

        if factory:
            di.factories[interface] = lambda x: service(**kwargs)
        else:
            di[interface] = service(**kwargs)


def configure_services(config: ConfigParser, implementations: dict):
    """
    Use configuration to bootstrap service implementations.

    --------
    Example:
    --------

    # Set some kwargs for a service
    di["var1"] = config["FOO"]["bar"]
    di["var2"] = config["BAR"]["foo"]

    # construct implementations with whatever config it needs
    thingy_kwargs = {"var1": di["var1"], "var2": di["var2"]}
    add_service(di, config, InterfaceOfThing, thing_label, service_as_passed_in, factory=True/False, **thingy_kwargs)
    """

    di.clear_cache()
    s = _Specifier(config, implementations)

    # Store Services
    s.add_service(interfaces.Store, "store")

    # Messenger Services
    s.add_service(interfaces.Messenger, "messenger")
