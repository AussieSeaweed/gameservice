from abc import ABC
from random import choice
from typing import Generic

from gameframe.game.tests import MonteCarloTestCaseMixin
from gameframe.sequential import SG


class SequentialMonteCarloTestCaseMixin(MonteCarloTestCaseMixin[SG], Generic[SG], ABC):
    """SequentialMonteCarloTestCaseMixin is the abstract base mixin for all sequential monte carlo test cases."""

    def test_monte_carlo(self) -> None:
        for i in range(self._monte_carlo_test_count):
            game: SG = self._create_game()

            while not game.terminal:
                choice(game.actor.actions).act()

            self._verify_game(game)
