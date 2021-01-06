from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

from gameframe.game import Game

__all__: Sequence[str] = ['MonteCarloTestCaseMixin']

G = TypeVar('G', bound=Game)


class MonteCarloTestCaseMixin(Generic[G], ABC):
    """MonteCarloTestCaseMixin is the abstract base mixin for all monte carlo test cases."""

    _test_count: int

    @abstractmethod
    def test_monte_carlo(self) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        pass

    @abstractmethod
    def _create_game(self) -> G:
        pass

    @abstractmethod
    def _verify(self, game: G) -> None:
        pass
