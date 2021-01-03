from abc import ABC, abstractmethod
from typing import Generic

from gameframe.game import G


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
    def _verify_game(self, game: G) -> None:
        pass
