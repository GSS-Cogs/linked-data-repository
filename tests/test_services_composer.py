from itertools import permutations
from types import MethodType
from unittest.mock import Mock

import pytest

from app.server import create_app
from app.services import NopStore
from app.services.inventory import INVENTORY

FALLEN_THROUGH = "An expected/required exception has failed to be thrown, this code should NEVER trigger"


def test_documentation_example():
    """
    Sanity check that the composable approach to testing
    with is working as per documentation
    """
    test_store = Mock
    test_store.get_record = MethodType(lambda x: {"mock": "record"}, test_store)

    app = create_app(store=test_store, sanic_test_mode=True)

    assert app.ctx.store.get_record() == {"mock": "record"}


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
