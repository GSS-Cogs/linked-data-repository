from sanic import Sanic, json
from websockets import WebSocketClientProtocol
import pytest
import requests
import asyncio
from logging import Logger
from mock import Mock
from app.auth import Auth
from app.utils.configuration.decorators import authorised


class TestDecorator:

    @pytest.mark.asyncio
    @pytest.yield_fixture
    def app(self):
        import random
        app = Sanic(name=str('_' + str(random.randint(0, 10000))))

        @app.route("/protected", methods=["GET"])
        async def protected(*args, **kwargs):
            return response.json({}, 204)

        yield app

    @pytest.fixture
    def test_cli(loop, app, test_server):
        """
            Run cli of the sanic app
        """
        return loop.run_until_complete(
            test_server(app))

    @pytest.mark.asyncio
    def test_no_user(self, app):
        """
        Test user not authenticated
        """

        func = Mock()
        decorated_auth_func = authorised(func)
        request, resp = app.test_client.get('/')
        dummy_response = decorated_auth_func(name='dummy_name')
        assert not func.called

    @pytest.mark.asyncio
    def test_user_authenticated(self, app):
        """
        Test user authenticated
        """
        func = Mock(return_value='ok')
        decorated_auth_func = authorised(func)
        dummy_request = app.test_client.request
        dummy_response = decorated_auth_func(dummy_request)
        assert dummy_response._mock_return_value == 'ok'
