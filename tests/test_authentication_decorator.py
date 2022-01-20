from sanic import Sanic
import pytest
import requests
import json
from logging import Logger
from app.auth import Auth


class TestDecorator:

    @pytest.fixture
    def app(self):
        import random
        app = Sanic(name=str('_' + str(random.randint(0, 10000))))
        return app

    @pytest.fixture
    def test_cli(loop, app, sanic_client):
        """
            Run cli of the sanic app
        """
        return loop.run_until_complete(sanic_client(app))

    def test_index_returns_200(self, app):
        request, response = app.test_client.get('/')
        assert response.status == 200

    def test_create_access_token(self):
        """

        """
        dummy_cfg = {'client_id': '',
                     'client_secret': '',
                     'redirect_uri': '',
                     'expiry_minutes': 120,
                     'encryption_key': '',
                     'algorithm': ''}

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

    def test_jwt_wrong_token(test_cli):
        """
            Test 'incorrect' JWT token and 'forbidden' response
        """
        dummy_token = ''
        dummy_JWT_header_key = ''
        dummy_JWT_header_prefix = ''
        resp = 'await'

        test_cli.get(
            '/protected',
            headers={
                dummy_JWT_header_key: f"{dummy_JWT_header_prefix} {dummy_token}"},
        )

        assert resp.status == 422

    def test_jwt_correct_token(test_cli):
        """
            Test 'Correct' JWT token with 'success' response
        """
        dummy_token = ''
        dummy_JWT_header_key = ''
        dummy_JWT_header_prefix = ''
        resp = 'await'
        # import pdb; pdb.set_trace()
        test_cli.get(
            '/protected',
            headers={
                dummy_JWT_header_key: f"{dummy_JWT_header_prefix} {dummy_token}"},
        )

        assert resp.status == 203
