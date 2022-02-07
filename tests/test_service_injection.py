import copy
from configparser import ConfigParser
from itertools import permutations
from types import MethodType

from kink import inject
import pytest

from app.server import create_app
from app.services import NopStore, NopMessenger, interfaces
from app.services.inventory import INVENTORY
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

    test_store = NopMessenger
    test_store.get_record = MethodType(lambda x: {"mock": "record"}, test_store)

    @inject
    def fake_endpoint(store: interfaces.Store):
        return store.get_record()

    assert fake_endpoint() == {"mock": "record"}


def test_configurable_implementations():
    """
    Implementations can be selected using just the configuration.ini
    """
    create_app(sanic_test_mode=True, config=nop_config)


def test_incorrect_interface_is_raised():
    """
    The expected exception is raised if an implementation does not
    support the required protocols.
    """

    class WrongUn:
        pass

    with pytest.raises(ProtocolError):
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


def test_all_implemntation_combinations_valid():
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
