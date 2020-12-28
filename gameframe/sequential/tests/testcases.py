from abc import ABC
from random import choice

from gameframe.game import E, N, P
from gameframe.game.tests import GameTestCaseMixin
from gameframe.sequential import G


class SequentialTestCaseMixin(GameTestCaseMixin[G, E, N, P], ABC):
    """SequentialTestCaseMixin is the abstract base mixin for all sequential test cases."""

    def test_monte_carlo(self) -> None:
        for i in range(self._num_monte_carlo_tests):
            game: G = self._create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            self._verify(game)
