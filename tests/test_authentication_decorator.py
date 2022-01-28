from sanic import Sanic
from websockets import WebSocketClientProtocol
import pytest
import pytest_asyncio
import requests
import json
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
    #
    # @pytest.fixture
    # def test_cli(loop, app, test_server):
    #     """
    #         Run cli of the sanic app
    #     """
    #     # import pdb; pdb.set_trace()
    #     return loop.run_until_complete(
    #         test_server(app))

    # @pytest.fixture
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

    @pytest.mark.asyncio
    async def test_fixture_test_client_get(app):
        """
        Test GET request
        """
        resp = app.test_client.get('/test_get')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"GET": True}

    @pytest.mark.asyncio
    async def test_fixture_test_client_post(app):
        """
        Test POST request
        """
        resp = app.test_client.post('/test_post')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"POST": True}

    @pytest.mark.asyncio
    async def test_fixture_test_client_put(app):
        """
        Test PUT request
        """
        resp = app.test_client.put('/test_put')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"PUT": True}

    @pytest.mark.asyncio
    async def test_fixture_test_client_delete(app):
        """
        Test DELETE request
        """
        resp = app.test_client.delete('/test_delete')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"DELETE": True}

    @pytest.fixture
    @pytest.mark.asyncio
    def test_create_access_token(self, mocker):
        """
        Test access token
        """
        dummy_cfg = {'client_id': '',
                     'client_secret': '',
                     'redirect_uri': '',
                     'expiry_minutes': 120,
                     'encryption_key': '',
                     'algorithm': ''}

        mock_cfg = mocker.patch.object(Auth.self.client, '')
        mock_cfg.return_value = 'dummy_client'
        with Auth(dummy_cfg, requests, Logger) as auth_manager:
            auth_manager.cfg['client_secret'] = "secret"
            auth_manager.cfg['client_id'] = "client_id"
            raw_token = auth_manager.get_access_token()

            assert raw_token == "access_token"

    @pytest.fixture
    @pytest.mark.asyncio
    def test_app_initialize(self, mocker):
        """
            Initialize the sanic app with JWT token
        """
        app = self.app()

        dummy_cfg = {'client_id': '',
                     'client_secret': '',
                     'redirect_uri': '',
                     'expiry_minutes': 120,
                     'encryption_key': '',
                     'algorithm': ''}

        mock_cookies = mocker.patch.object(Auth.self.cookie, '')
        mock_cookies.return_value = 'dummy_cookie'
        with Auth(dummy_cfg, requests, Logger) as auth_manager:
            auth_manager.cfg['client_secret'] = "secret"
            auth_manager.cfg['client_id'] = "client_id"

            @app.route("/protected", methods=["GET"])
            async def protected(*args, **kwargs):
                return json({}, 204)

            yield app

    @pytest.mark.asyncio
    async def test_jwt_wrong_token(app):
        """
            Test 'incorrect' JWT token and 'forbidden' response
        """
        dummy_token = ''
        dummy_JWT_header_key = ''
        dummy_JWT_header_prefix = ''

        resp = await app.test_client.get(
            '/protected',
            headers={
                dummy_JWT_header_key: f"{dummy_JWT_header_prefix} {dummy_token}"},
        )

        assert resp.status == 422

    @pytest.mark.asyncio
    def test_jwt_correct_token(app):
        """
            Test 'Correct' JWT token with 'success' response
        """
        dummy_token = ''
        dummy_JWT_header_key = ''
        dummy_JWT_header_prefix = ''

        resp = app.test_client.get(
            '/protected',
            headers={
                dummy_JWT_header_key: f"{dummy_JWT_header_prefix} {dummy_token}"},
        )

        assert resp.status == 203
