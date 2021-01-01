from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from gameframe.game import G


class MonteCarloTestCaseMixin(Generic[G], ABC):
    """MonteCarloTestCaseMixin is the abstract base mixin for all monte carlo test cases."""

    @abstractmethod
    def test_monte_carlo(self: MonteCarloTestCaseMixin[G]) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        pass

    @abstractmethod
    def _create_game(self: MonteCarloTestCaseMixin[G]) -> G:
        pass

    @abstractmethod
    def _verify(self: MonteCarloTestCaseMixin[G], game: G) -> None:
        pass

    @property
    @abstractmethod
    def _num_monte_carlo_tests(self: MonteCarloTestCaseMixin[G]) -> int:
        pass
