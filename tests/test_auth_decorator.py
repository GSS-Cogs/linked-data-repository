import os
from unittest import mock
from sanic import Sanic
import pytest
import random
from app.utils.auth.decorator import decorator



class TestDecorator:
    @pytest.fixture

    def app(self):
        app = Sanic(name=str("_" + str(random.randint(0, 10000))))
        yield app

    @pytest.fixture(autouse=True)
    def mock_settings_env_vars(self):
        with mock.patch.dict(os.environ, {"OAUTH_DOMAIN": "www.test.com",
                                          "OAUTH_CLIENT_ID": "DUMMY_CLIENT_ID",
                                          "OAUTH_CLIENT_SECRET": "DUMMY_CLIENT_SECRET",
                                          "OAUTH_REDIRECT_URI": "www.test.com"}):
            yield

    def test_decorator_requires_one_of(self):
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ONE or more of them.
        """


    def test_decorator_requires_all(self):
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ALL of them.
        """
        ...

    def test_failed_auth_is_redirected(self):
        """
        Test that a faield authorization is redirected to the
        keyword specified uri.
        """
        ...

    def test_variable_response_endpoint_has_auth(self):
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has auth scenario.
        """
        ...

    def test_variable_response_endpoint_has_no_auth(self):
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has no auth scenario.
        """
        ...
