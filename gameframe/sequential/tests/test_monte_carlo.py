from abc import ABC, abstractmethod
from random import choice
from typing import Generic, TypeVar

from gameframe.sequential.bases import BaseSeqGame

G = TypeVar('G', bound=BaseSeqGame)


class MCTestCaseMixin(Generic[G], ABC):
    """MCTestCaseMixin is the abstract base mixin for all monte carlo test cases."""

    @property
    @abstractmethod
    def _test_count(self) -> int:
        pass

    def test_monte_carlo(self) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        for i in range(self._test_count):
            game = self._create_game()

            while game.env.actor is not None:
                choice(game.env.actor.actions).act()
                self._verify(game)

    @abstractmethod
    def _create_game(self) -> G:
        pass

    def _verify(self, game: G) -> None:
        if game.is_terminal:
            assert game.env.actor is None
        else:
            assert game.env.actor is not None

            if game.nature is not game.env.actor:
                assert not game.nature.actions

            for player in game.players:
                if player is not game.env.actor:
                    assert not player.actions
