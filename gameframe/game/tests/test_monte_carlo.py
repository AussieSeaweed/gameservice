from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from gameframe.game.bases import BaseGame

G = TypeVar('G', bound=BaseGame)


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
        pass

    @abstractmethod
    def act(self, game: G) -> None:
        pass

    @abstractmethod
    def create_game(self) -> G:
        pass
