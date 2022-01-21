from abc import ABCMeta, abstractmethod


class BaseStore(metaclass=ABCMeta):
    """
    Generic base class for our store provider.
    """

    @abstractmethod
    def setup(self, *args, **kwargs):
        """
        Generic setup method by all store implemetations.

        Where no setup is required, a pass with no return implementation
        is acceptable.
        """
        pass
