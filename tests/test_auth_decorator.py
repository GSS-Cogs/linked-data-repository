import os
from unittest import mock
from sanic import Sanic
from sanic_testing import TestManager
from sanic.response import json
import pytest
import random
import asyncio
import logging
import requests
# from .server import app
from app.utils.auth import decorator
from app.utils.auth.decorator import auth
from app.utils.auth.manager import AuthManager


class TestDecorator:

    @pytest.yield_fixture
    def app(self):
        app = Sanic(name=str("_" + str(random.randint(0, 10000))))
        app.config['KEEP_ALIVE_TIMEOUT'] = 60

        @app.get("/test_one_of")
        @auth(requires_one_of=['admin'])
        async def test_one_of(request):
            return json({'ok': True})

        @app.get("/test_requires_all")
        @auth(requires_all=['admin'])
        async def test_requires_all(request):
            return json({'ok': True})

        @app.get("/failed_redirects")
        @auth(requires_all=['admin'], redirect_to="/not_allowed")
        async def test_request_failed(request):
            return json({'ok': True})

        @app.get("/not_allowed")
        async def test_not_allowed(request):
            return json({'ok': True})

        @app.get("/auth_might_be_allowd")
        @auth()
        async def test_might_be_allowed(auth: AuthManager, request):
            if auth._has_role("admin"):
                return text(
                    'I\'m the version of the "maybe-auth" endpoint for people with the "admin" role!'
                )
            else:
                return text(
                    'I\'m the version of the "maybe-auth" endpoint for people without the "admin" role!'
                )

        yield app

    @pytest.fixture
    def test_cli(loop, app, test_client):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(test_client(app))

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

        request, response = app.test_client.get("/test_one_of")
        assert response.status_code == 200

    def test_decorator_requires_all(self, app):
        """
        When you decorated an endpoing with one or more
        roles, has auth if user has ALL of them.
        """

        request, response = app.test_client.post('/test_requires_all"')
        assert response.status_code == 200

    def test_failed_auth_is_redirected(self, app):
        """
        Test that a faield authorization is redirected to the
        keyword specified uri.
        """

        decorated_func = auth(requires_one_of=['blah'])
        request, response = app.test_client.post('/failed_redirects')
        assert response.status_code == 200

    def test_variable_response_endpoint_has_auth(self, app):
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has auth scenario.
        """

        request, response = app.test_client.post('/auth_might_be_allow')
        assert response.status_code == 200

    def test_variable_response_endpoint_has_no_auth(self, app):
        """
        Endpoint gives a response but that response varies based
        on auth - this is the has no auth scenario.
        """
        request, response = app.test_client.post('/failed_redirects')
        assert response.status_code == 200
