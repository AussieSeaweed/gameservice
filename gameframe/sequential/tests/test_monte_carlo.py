from abc import ABC, abstractmethod
from random import choice
from typing import Generic

from gameframe.game.bases import N, P
from gameframe.sequential import SeqGame
from gameframe.sequential.bases import E


class MCTestCaseMixin(Generic[E, N, P], ABC):
    """MCTestCaseMixin is the abstract base mixin for all monte carlo test
    cases.
    """

    @property
    @abstractmethod
    def _test_count(self) -> int:
        pass

    def test_monte_carlo(self) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any
        tests
        """
        for i in range(self._test_count):
            game = self._create_game()

            while game.env.actor is not None:
                choice(game.env.actor.actions).act()
                self._verify(game)

    @abstractmethod
    def _create_game(self) -> SeqGame[E, N, P]:
        pass

    @abstractmethod
    def _verify(self, game: SeqGame[E, N, P]) -> None:
        pass
