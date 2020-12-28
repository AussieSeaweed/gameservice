from abc import ABC, abstractmethod


class TestCaseMixin(ABC):
    """TestCaseMixin is the abstract base class for all game test mixins."""

    @staticmethod
    @abstractmethod
    def _create_game():
        pass

    @staticmethod
    @abstractmethod
    def _verify(game):
        pass
