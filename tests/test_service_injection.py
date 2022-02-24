import copy
from configparser import ConfigParser
from itertools import permutations
from sys import implementation
from types import MethodType

from kink import inject, di
import pytest

from app.server import create_app
from app.services import NopStore, interfaces
from app.services.inventory import INVENTORY
from app.services.container import Injector
from app.services.container import ProtocolError, UnknownImplementationError


nop_config = ConfigParser()
nop_config.add_section("STORE")
nop_config["STORE"]["default_implementation"] = "Nop"
nop_config.add_section("MESSENGER")
nop_config["MESSENGER"]["default_implementation"] = "Nop"


def test_documentation_example():
    """
    Sanity check that the documented test example works
    """

    test_store = NopStore
    test_store.get_record = MethodType(lambda x: {"mock": "record"}, test_store)

    @inject
    def fake_endpoint(store: interfaces.Store):
        return store.get_record()

    inj: Injector = Injector(nop_config)
    inj.configure_service(interfaces.Store, "store", {})

    assert fake_endpoint() == {"mock": "record"}


def test_dependencies_can_be_configured():
    """
    Check that we can pass configuration
    through the dependency injection framework.
    """

    @inject(alias=interfaces.Store)
    class TestStore:
        """
        A test store that holds on to whatever kwargs
        get passed to it
        """

        def __init__(self, **kwargs):
            self.kwargs = kwargs

    # Instanitate injector with implementations specified
    inj: Injector = Injector(nop_config, {'store': TestStore})

    # Set configuration
    inj.configure_service(interfaces.Store, "store", {"kwargy": "foo"})

    @inject
    def get_me_an_injected_store(store: interfaces.Store) -> interfaces.Store:
        return store

    # Our TestStore implementation has access to said configuration
    instantiated_store = get_me_an_injected_store()
    assert instantiated_store.kwargs['kwargy'] == 'foo'


def test_not_a_factory():
    """
    Confirm that where a factory is not specified, the
    service in question is only instantiated once even when
    an @inject decorated function is called multiple times.
    """

    @inject(alias=interfaces.Store)
    class NotAFactoryStore:
        """
        A test store thats not using a factory pattern
        """
        pass

    # Instanitate injector
    inj: Injector = Injector(nop_config, {'store': NotAFactoryStore})
    inj.configure_service(interfaces.Store, "store", {})

    @inject
    def get_me_a_non_factory_store(store: interfaces.Store) -> interfaces.Store:
        return store

    # Instantiating twice gets us exaactly the same object back
    instantiated_store_1 = get_me_a_non_factory_store()
    instantiated_store_2 = get_me_a_non_factory_store()
    assert instantiated_store_1 is instantiated_store_2


def test_is_a_factory():
    """
    Confirm that services where a factory is specified, the
    service in question is a new object each time an @inject
    decorated function is called.
    """

    @inject(alias=interfaces.Store, use_factory=True)
    class IsAFactoryStore:
        """
        A test store that is using a factory pattern
        """
        pass

    # Instanitate injector
    inj: Injector = Injector(nop_config, {'store': IsAFactoryStore})
    inj.configure_service(interfaces.Store, "store", {})

    @inject
    def get_me_a_factory_store(store: interfaces.Store) -> interfaces.Store:
        return store

    # Instantiating twice gets us different objects back
    instantiated_store_1 = get_me_a_factory_store()
    instantiated_store_2 = get_me_a_factory_store()
    assert instantiated_store_1 is not instantiated_store_2


def test_configurable_implementations():
    """
    Implementations can be selected using just the configuration.ini
    """
    create_app(sanic_test_mode=True, config=nop_config)

# TODO - see NOTE in method body.
@pytest.mark.skip(reason="Cannot fail until we've defined our first protocol with methods")
def test_incorrect_interface_is_raised():
    """
    The expected exception is raised if an implementation does not
    support the required protocols.
    """

    class WrongUn:
        pass

    with pytest.raises(ProtocolError):
        # NOTE: When we have out first interface with methods, pass "WrongUn"
        # to it (as currently per messenger) and remove skip decorator.
        create_app(messenger=WrongUn, sanic_test_mode=True, config=nop_config)

def test_bad_config_raises():
    """
    Specifying unknown implementations via configuration raises an appropriate
    exception.
    """

    config = copy.deepcopy(nop_config)
    config["STORE"]["default_implementation"] = "I'm not a thing that exists"

    with pytest.raises(UnknownImplementationError):
        create_app(sanic_test_mode=True, config=config)


def test_all_implementation_combinations_valid():
    """
    Test that the app can be instantiated with
    all combinations implementations as defined
    in app.services.inventory.INVENTORY.
    """

    all_permutations = permutations(
        (
            {"store": x for x in INVENTORY["store"].values()},
            {"messenger": x for x in INVENTORY["messenger"].values()},
        )
    )

    for a_permutation in all_permutations:
        kwargs = {}
        for implementation_map in a_permutation:
            assert len(implementation_map) == 1
            for k, v in implementation_map.items():
                assert k not in kwargs
                kwargs[k] = v

        try:
            create_app(**kwargs, sanic_test_mode=True)
        except Exception as err:
            raise Exception(
                f"Unable to instantiate app with specified services: \n{kwargs}"
            ) from err
