from sanic import Sanic
from websockets import WebSocketClientProtocol
import pytest
import requests
import json
from logging import Logger
from app.auth import Auth


class TestDecorator:

    @pytest.mark.asyncio
    @pytest.fixture
    def app(self):
        import random
        app = Sanic(name=str('_' + str(random.randint(0, 10000))))

        @app.route("/protected", methods=["GET"])
        async def protected(*args, **kwargs):
            return json({}, 204)

        yield app

    @pytest.fixture
    def test_cli(loop, app, sanic_client):
        """
            Run cli of the sanic app
        """

        return loop.run_until_complete(
            sanic_client(app, protocol=WebSocketClientProtocol))

    @pytest.mark.asyncio
    async def test_fixture_test_client_get(test_cli):
        """
        Test GET request
        """

        resp = await test_cli.get('/test_get')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"GET": True}

    @pytest.mark.asyncio
    async def test_fixture_test_client_post(test_cli):
        """
        Test POST request
        """
        resp = await test_cli.post('/test_post')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"POST": True}

    @pytest.mark.asyncio
    async def test_fixture_test_client_put(test_cli):
        """
        Test PUT request
        """
        resp = await test_cli.put('/test_put')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"PUT": True}

    @pytest.mark.asyncio
    async def test_fixture_test_client_delete(test_cli):
        """
        Test DELETE request
        """
        resp = await test_cli.delete('/test_delete')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"DELETE": True}

    @pytest.fixture
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

    @pytest.fixture
    async def test_jwt_wrong_token(test_cli):
        """
            Test 'incorrect' JWT token and 'forbidden' response
        """
        dummy_token = ''
        dummy_JWT_header_key = ''
        dummy_JWT_header_prefix = ''

        resp = await test_cli.get(
            '/protected',
            headers={
                dummy_JWT_header_key: f"{dummy_JWT_header_prefix} {dummy_token}"},
        )

        assert resp.status == 422

    @pytest.mark.asyncio
    def test_jwt_correct_token(test_cli):
        """
            Test 'Correct' JWT token with 'success' response
        """
        dummy_token = ''
        dummy_JWT_header_key = ''
        dummy_JWT_header_prefix = ''

        resp = test_cli.get(
            '/protected',
            headers={
                dummy_JWT_header_key: f"{dummy_JWT_header_prefix} {dummy_token}"},
        )

        assert resp.status == 203
