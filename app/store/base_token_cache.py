from abc import ABCMeta, abstractmethod
from enum import Enum
from pathlib import Path
from typing import List, Union


class BaseTokenCache(metaclass=ABCMeta):
    """
        Abstract class defining the token cache store and access/upload token data per user

        Notes: Temporary use TinyDB with a view to using a more stable solution in prod
    """

    def __init__(self):
        pass

    @abstractmethod
    def setup(self, *args, **kwargs):
        """
        Generic setup method to allow for the use of more
        complex database solutions.
        """
        pass

    @abstractmethod
    def insert_token(self, user=None, token=None):
        """
        Insert and store token per user:
            - insert_token(user='dummy_user', token='dummy_token')
        """
        pass

    @abstractmethod
    def fetch_token(self, user=None) -> dict:
        """
        Fetch token per user:
            - fetch_token(user='dummy_user')
        """

        pass
