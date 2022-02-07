from sanic import Sanic
import pytest
import random
from unittest.mock import Mock

from app.utils import auth, AuthManager


class TestDecorator:
    @pytest.mark.asyncio
    @pytest.yield_fixture
    def app(self):
        app = Sanic(name=str("_" + str(random.randint(0, 10000))))
        yield app

    def test_decorator_requires_one_of():
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ONE or more of them.
        """
        ...

    def test_decorator_requires_all():
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ALL of them.
        """
        ...


    def test_failed_auth_is_redirected():
        """
        Test that a faield authorization is redirected to the
        keyword specified uri.
        """
        ...


    def test_variable_response_endpoint_has_auth():
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has auth scenario.
        """
        ...

    def test_variable_response_endpoint_has_no_auth():
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has no auth scenario.
        """
        ...
