import copy
from itertools import permutations
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import MethodType
from unittest.mock import Mock

import pytest

from app.server import create_app, ProtocolError
from app.services.inventory import INVENTORY
from app.services.container import UnknownImplementationError

FALLEN_THROUGH = "An expected/required exception has failed to be thrown, this code should NEVER trigger"


def test_documentation_example():
    """
    Sanity check that the composable approach to testing
    is working as per documentation
    """
    test_store = Mock
    test_store.get_record = MethodType(lambda x: {"mock": "record"}, test_store)

    app = create_app(store=test_store, sanic_test_mode=True)

    assert app.ctx.store.get_record() == {"mock": "record"}


def test_incorrect_interface_is_raised():
    """
    The expected exception is raised if an implementation does not
    support the required protocols.
    """

    class WrongUn:
        pass

    with pytest.raises(ProtocolError):
        create_app(messenger=WrongUn, sanic_test_mode=True)


def test_configurable_implementations():
    """
    Implementations can be selected using just the configuration.ini
    """

    config_path = Path(
        Path(__file__).parent / "fixtures" / "configuration" / "nop_config.ini"
    )
    create_app(sanic_test_mode=True, config_path=config_path)


def test_bad_config_raises():
    """
    Specifying unknown implementations via configuration raises an appropriate
    exception.
    """

    config_path = Path(
        Path(__file__).parent / "fixtures" / "configuration" / "bad_config.ini"
    )
    with pytest.raises(UnknownImplementationError):
        create_app(sanic_test_mode=True, config_path=config_path)


def test_all_implemntation_combinations_valid():
    """
    Test that the app can be instantiated with
    all combinations of currently defined implementations.
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
