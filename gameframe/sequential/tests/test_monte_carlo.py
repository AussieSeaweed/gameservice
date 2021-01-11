from abc import ABC
from random import choice

from gameframe.game.tests import MonteCarloTestCaseMixin


class SequentialMonteCarloTestCaseMixin(MonteCarloTestCaseMixin, ABC):
    """SequentialMonteCarloTestCaseMixin is the abstract base mixin for all sequential monte carlo test cases."""

    def test_monte_carlo(self):
        for i in range(self._test_count):
            game = self._create_game()

            while not game.is_terminal:
                choice(game.actor.actions).act()

            self._verify(game)
