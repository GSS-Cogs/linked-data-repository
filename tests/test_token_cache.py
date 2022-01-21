import pytest
from app.store.base_token_cache import BaseTokenCache


class TestTokenCache:
    """
        Test the Token cache abstract class and associated methods
    """

    def test_set_up(self):
        """
        Test and assert abstract method has setup
        """

        dummy_class = BaseTokenCache
        assert hasattr(dummy_class, 'setup')

    def test_insert_token(self):
        """
        Test and assert abstract method has inset token
        """
        dummy_class = BaseTokenCache
        assert hasattr(dummy_class, 'insert_token')

    def test_fetch_token(self):
        """
        Test and assert abstract method has fetch token
        """
        dummy_class = BaseTokenCache
        assert hasattr(dummy_class, 'fetch_token')
