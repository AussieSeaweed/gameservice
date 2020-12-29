from abc import ABC
from random import choice

from gameframe.game.tests import GameTestCaseMixin


class SequentialTestCaseMixin(GameTestCaseMixin, ABC):
    """SequentialTestCaseMixin is the abstract base mixin for all sequential test cases."""

    def test_monte_carlo(self):
        for i in range(self._num_monte_carlo_tests):
            game = self._create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            self._verify(game)
