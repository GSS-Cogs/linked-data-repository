from abc import ABCMeta, abstractmethod


class BaseMessager(metaclass=ABCMeta):
    """
    Generic base class for our messager provider.
    """

    @abstractmethod
    def setup(self, *args, **kwargs):
        """
        Generic setup method required by all messager implemetations.

        Where no setup is required, a pass with no return implementation
        is acceptable.
        """
        pass
