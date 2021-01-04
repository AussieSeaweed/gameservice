from abc import ABC
from random import choice
from typing import TypeVar, final

from gameframe.game.tests import MonteCarloTestCaseMixin
from gameframe.sequential import SequentialGame
from gameframe.utils import override

__all__ = ['SequentialMonteCarloTestCaseMixin']

SG = TypeVar('SG', bound=SequentialGame)


class SequentialMonteCarloTestCaseMixin(MonteCarloTestCaseMixin[SG], ABC):
    """SequentialMonteCarloTestCaseMixin is the abstract base mixin for all sequential monte carlo test cases."""

    @final
    @override
    def test_monte_carlo(self) -> None:
        for i in range(self._test_count):
            game: SG = self._create_game()

            while not game.terminal:
                choice(game.actor.actions).act()

            self._verify_game(game)
