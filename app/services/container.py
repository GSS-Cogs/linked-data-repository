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
        self.msg = f'Implementation "{label}" not found for service: "{service}"'


def add_service(
    config,
    interface,
    service_label: str,
    declaration: Union[str, Type[T], None],
    factory=False,
    **kwargs,
):
    """
    di (direct injection containwer) wrapper: allows service instantiation
    from a str name (such as when acquired from the config) and as either a
    singleton or factory.
    """

    # Set default, where None is declared
    if not declaration:
        declaration = config[service_label.upper()]["default_implementation"]

    # If str not class, get the class from the inventory
    service = (
        INVENTORY[service_label][declaration]
        if isinstance(declaration, str)
        else declaration
    )

    if factory:
        di.factories[interface] = lambda x: service(**kwargs)
    else:
        di[interface] = service(**kwargs)


def configure_services(config: ConfigParser, **service_kwargs) -> (Sanic):
    """
    Use the app configuration to bootstrap service implementations.

    --------
    Example:
    --------

    # Set some kwargs for a service
    di["var1"] = app.ctx.config["FOO"]["bar"]
    di["var2"] = app.ctx.config["BAR"]["foo"]

    # construct implementations with whatever config it needs
    thingy_kwargs = {"var1": di["var1"], "var2": di["var2"]}
    add_service(di, config, InterfaceOfThing, thing_label, service_as_passed_in, factory=True/False, **thingy_kwargs)

    TODO: example is confusing, do we need so pass those kwargs to
    # the di before the implementation? Try it and find out.
    """

    di.clear_cache()

    # Store Services
    add_service(config, interfaces.Store, "store", service_kwargs["store"])

    # Messenger Services
    add_service(
        config, interfaces.Messenger, "messenger", service_kwargs["messenger"]
    )
