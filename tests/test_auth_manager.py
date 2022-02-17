# TODO - tests for app.utils.auth.manager.AuthManager
import os
import hashlib
from unittest import mock
from sanic import Sanic
import pytest
import random
import requests
from logging import Logger
from app.utils.auth.manager import AuthManager


class TestManager:
    @pytest.fixture
    def test_sanity(self):
        assert(1 + 1, 2)

    def test_encrypt_cookie(self):
        """
        Cookie can be enrypted
        """
        dummy_cfg = {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'expiry_minutes': 120,
            'encryption_key': '',
            'algorithm': hashlib.sha256(
                'dummy_algo'.encode('utf-8')).hexdigest()}

        requests.cookies = {"user": "dummy_user"}
        dummy_auth_manager = AuthManager(dummy_cfg, requests, Logger)
        dummy_encrypt_cookie = dummy_auth_manager.encrypt_cookie({'msg':'ss'})
        assert(dummy_encrypt_cookie, {})

    def test_decrypt_cookie(self):
        """
        Cookie can be decrypted
        """
        dummy_cfg = {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'expiry_minutes': 120,
            'encryption_key': '',
            'algorithm': hashlib.sha256(
                'dummy_algo'.encode('utf-8')).hexdigest()}

        requests.cookies = {"user": "dummy_user"}
        dummy_auth_manager = AuthManager(dummy_cfg, requests, Logger)
        dummy_decrypt_cookie = dummy_auth_manager.decrypt_cookie()
        assert(dummy_decrypt_cookie, {})
    #
