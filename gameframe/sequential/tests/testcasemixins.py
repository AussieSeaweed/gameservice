from abc import ABC, abstractmethod
from random import choice

from gameframe.game.tests import TestCaseMixin


class SequentialTestCaseMixin(TestCaseMixin, ABC):
    """SequentialTestCaseMixin is the abstract base class for all sequential test mixins."""

    @property
    @abstractmethod
    def _num_monte_carlo_tests(self):
        pass

    def test_monte_carlo(self):
        """Runs monte carlo tests of sequential games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        for i in range(self._num_monte_carlo_tests):
            game = self._create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            assert self._verify(game)
