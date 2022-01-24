from itertools import permutations
from unittest.mock import Mock

import pytest

from app.server import create_app
from app.services import Composer
from app.services.compose import UnknownDriverError
from app.services.store.implementations import NopStore
from app.services.inventory import INVENTORY

FALLEN_THROUGH = "An expected/required exception has failed to be thrown, this code should NEVER trigger"


def test_documentation_example():
    """
    Sanity check that the composable approach to testing
    with drivers is working as per documentation
    """
    test_store = NopStore()

    test_store.get_record = lambda: {"mock": "record"}

    app = create_app(store=test_store, sanic_test_mode=True, enforce_base_classes=False)

    assert app.ctx.store.get_record() == {"mock": "record"}


def test_drivers_must_be_correct_type():
    """
    Where drivers are being passed in, those classes
    _must_ have the correct Base type.
    """
    not_a_messager_driver = NopStore()
    expectation_met = False
    try:
        create_app(messager=not_a_messager_driver, sanic_test_mode=True)
    except TypeError as err:
        assert "does not but should have parent class" in str(err)
        expectation_met = True
    assert expectation_met, FALLEN_THROUGH


def test_all_instantiated_driver_combinations_valid():
    """
    Test that the app can be instantiated with
    all combinations of currently defined drivers.
    """

    all_permutations = permutations(
        (
            {"store": x for x in INVENTORY["store"].values()},
            {"messager": x for x in INVENTORY["messager"].values()},
        )
    )

    for a_permutation in all_permutations:
        kwargs = {}
        for driver in a_permutation:
            assert len(driver) == 1
            for k, v in driver.items():
                assert k not in kwargs
                kwargs[k] = v()
                kwargs[k].setup()

        try:
            create_app(**kwargs, sanic_test_mode=True)
        except Exception as err:
            raise Exception(
                f"Unable to instantiate app with provided drivers: \n{kwargs}"
            ) from err


def test_compose_fails_with_unknown_driver_label():
    """
    Test that passing unknown labels to the compose
    functions generate the expected error.
    """
    
    composer = Composer('', True)

    with pytest.raises(UnknownDriverError):
        composer.store("im not a driver!!!")

    with pytest.raises(UnknownDriverError):
        composer.messager("im not a driver!!!")
