from abc import ABC, abstractmethod
from typing import Generic

from gameframe.game import BaseActor, BaseGame
from gameframe.game._generics import G


class MCTestCaseMixin(Generic[G], ABC):
    MC_TEST_COUNT: int

    def test_monte_carlo(self) -> None:
        for i in range(self.MC_TEST_COUNT):
            game = self.create_game()
            self.verify(game)

            while not game.terminal:
                self.act(game)
                self.verify(game)

    def verify(self, game: G) -> None:
        assert isinstance(game, BaseGame)
        assert isinstance(game.nature, BaseActor)
        assert all(isinstance(player, BaseActor) for player in game.players)

    @abstractmethod
    def act(self, game: G) -> None:
        pass

    @abstractmethod
    def create_game(self) -> G:
        pass
