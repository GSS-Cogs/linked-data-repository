from itertools import permutations

import pytest

from app.server import create_app
from app.services import compose
from app.services.inventory import STORES, MESSAGERS
from app.services.store.drivers import NopStore

FALLEN_THROUGH = "An expected/required exception has failed to be thrown, this code should NEVER trigger"


def test_documentation_example():
    """
    Sanity check that the composable approach to testing
    with drivers is working as per documentation
    """
    nop_store = NopStore()

    nop_store.get_record = lambda: {"mock": "record"}

    app = create_app(store=nop_store, test_mode = True)

    assert app.ctx.store.get_record() == {"mock": "record"}


def test_drivers_must_be_correct_type():
    """
    Where drivers are being passed in, those classes
    _must_ have the correct Base type.
    """
    not_a_messager_driver = NopStore()
    expectation_met = False
    try:
        create_app(messager=not_a_messager_driver, test_mode = True)
    except TypeError as err:
        assert "does not but should have parent class" in str(err)
        expectation_met = True
    assert expectation_met, FALLEN_THROUGH


def test_drivers_must_be_instantiated():
    """
    Where drivers are being passed in, those classes
    _must_ be instantiated.
    """
    non_instantiated_store = NopStore
    expectation_met = False
    try:
        create_app(store=non_instantiated_store, test_mode = True)
    except AssertionError as err:
        assert " is not but should have been instantiated" in str(err)
        expectation_met = True
    assert expectation_met, FALLEN_THROUGH


def test_all_instantiated_driver_combinations_valid():
    """
    Test that the app can be instantiated with
    all combinations of currently defined drivers.
    """

    all_permutations = permutations(
        (
            {"store": x for x in STORES.values()},
            {"messager": x for x in MESSAGERS.values()},
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
            create_app(**kwargs, test_mode = True)
        except Exception as err:
            raise Exception(
                f"Unable to instantiate app with provided drivers: \n{kwargs}"
            ) from err
