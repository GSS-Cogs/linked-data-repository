from configparser import ConfigParser
from typing import Type, TypeVar, Union

from kink import di

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
    """

    def __init__(self, config: ConfigParser, implementations: dict = {}):
        self.config = config
        self.implementations = implementations
        di.clear_cache()

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

    di.clear_cache()
    inj = Injector(config, implementations)

    # Configure stores
    configuration_store = {}
    inj.configure_service(interfaces.Store, "store", configuration_store)

    # Configure messengers
    configuration_messenger = {}
    inj.configure_service(interfaces.Messenger, "messenger", configuration_messenger)
