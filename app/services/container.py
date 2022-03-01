from configparser import ConfigParser
from typing import Optional, Type, Union

from kink import di, Container

from . import interfaces
from .inventory import INVENTORY


class UnknownImplementationError(Exception):
    """
    Raised where we are specifying an unknown implementation.
    """

    def __init__(self, service: str, label: str):
        self.msg = f'Implementation "{label}" not found for service: "{service}"'


class ProtocolError(Exception):
    """
    Raised where an implementation does not meet the required protocols.
    """

    def __init__(self, msg):
        self.msg = msg


class Injector:
    """
    di (direct injection container) wrapper: allows:

    * service instantiation from a str name
    * instantiation as singleton or factory
    * runtime validation of required protocols

    :config: A ConfigParser object used to specify the
    default implementation from the inventory.

    :implentations: A dictionary of specified implementations
    where passed in at runtime.

    :enforce_protocols: used to flag off the type
    check (TESTING ONLY).
    """

    def __init__(
        self,
        config: Optional[ConfigParser] = None,
        implementations: dict = {},
        enforce_protocols=True
    ):
        self.config = config
        self.implementations = implementations
        self.enforce_protocols = enforce_protocols

    @staticmethod
    def _test_only_reset_container():
        """
        Resets all the cached Container (di) information as already defined
        in global state.

        This is sometimes necessary for testing as it's a scenario where we'd
        specify multiple "use this" implementations for a given interface
        (something that cant happen in production), hence we need a test mode
        reset.

        If you use this helper anywhere other than at the start of a test
        you are 100% doing it wrong.
        """

        global di
        di.clear_cache()
        di._factories = {}
        di._services = {}

    def configure_service(
        self,
        interface: Type,
        service_label: str,
        config_dict,
    ):
        """
        Configure a single service within the container, making it accesible
        under a keyword equal to the required interface, i.e:
        `di[interfaces.Store] = <STORE WE'RE USING>`

        Configuration in the form of a keyword dictionary is passed in and
        will be avabilable to the chosen implementation at runtime.
        """

        # decaration is the implentation that's been specified for injection
        declaration: Union[str, Type] = self.implementations.get(service_label, None)

        # Where declaration is None, we're going with the default from the config
        if not declaration:
            if not self.config:
                raise ValueError(
                    f'Aborting. Service "{service_label}" must have either an explicit '
                    " implementation passed in or a default set via config. You have neither."
                )
            declaration = self.config[service_label.upper()]["default_implementation"]

        # If declaration is str not class, get the class from the inventory
        try:
            if isinstance(declaration, str):
                service = INVENTORY[service_label][declaration]
            else:
                service = declaration
        except KeyError:
            raise UnknownImplementationError(service_label, declaration)

        # Confirm that whatevers been specified has the correct protocols
        # We should ONLY ever flag this off for testing
        if self.enforce_protocols:
            msg = "{} does not implemented protocols of {}"
            if not isinstance(service, interface):
                raise ProtocolError(msg.format(service, interface))

        # Propogate configuration to constructors
        if service in di._factories:
            di.factories[interface] = lambda x: service(**config_dict)
        else:
            di[interface] = service(**config_dict)


def configure_services(config: ConfigParser, implementations: dict):
    """
    Configure all services and the configuration to pass to each service.
    """

    inj = Injector(config, implementations)

    # Configure stores
    configuration_store = {}
    inj.configure_service(interfaces.Store, "store", configuration_store)

    # Configure messengers
    configuration_messenger = {}
    inj.configure_service(interfaces.Messenger, "messenger", configuration_messenger)
