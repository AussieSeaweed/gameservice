from abc import ABC, abstractmethod
from typing import Generic

from gameframe.game import E, G, N, P


class GameTestCaseMixin(Generic[G, E, N, P], ABC):
    """GameTestCaseMixin is the abstract base mixin for all game test cases."""

    @abstractmethod
    def test_monte_carlo(self) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        pass

    @staticmethod
    @abstractmethod
    def _create_game() -> G:
        pass

    @property
    @abstractmethod
    def _num_monte_carlo_tests(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    def _verify(game: G) -> None:
        pass
