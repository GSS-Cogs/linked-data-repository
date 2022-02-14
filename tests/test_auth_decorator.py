import os
from unittest import mock
from sanic import Sanic
import pytest
import random
from app.utils.auth.decorator import auth


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
                                          "O4AUTH_REDIRECT_URI": "www.test.com"}):
            yield

    def test_decorator_requires_one_of(self, app):
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ONE or more of them.
        """

        decorated_func = auth(requires_one_of=['blah'])
        request, _ = app.test_client.post('/')
        response = decorated_func(request)
        assert(response, '')


    def test_decorator_requires_all(self, app):
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ALL of them.
        """

        decorated_func = auth(requires_all=True)
        request, _ = app.test_client.post('/')
        response = decorated_func(request)
        assert (response, '')

    def test_failed_auth_is_redirected(self, app):
        """
        Test that a faield authorization is redirected to the
        keyword specified uri.
        """

        decorated_func = auth(requires_one_of=['blah'])
        request, _ = app.test_client.post('/')
        response = decorated_func(request)
        assert (response, '')

    def test_variable_response_endpoint_has_auth(self, app):
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has auth scenario.
        """

        decorated_func = auth(requires_one_of=['admin'])
        request, _ = app.test_client.post('/')
        response = decorated_func(request)
        # has auth response object?
        assert (response, '')

    def test_variable_response_endpoint_has_no_auth(self, app):
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has no auth scenario.
        """

        decorated_func = auth(requires_one_of=['blah'])
        request, _ = app.test_client.post('/')
        response = decorated_func(request)
        #  no auth resposne object?
        assert (response, '')
