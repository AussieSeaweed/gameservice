from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from gameframe.sequential.bases import BaseSeqGame

G = TypeVar('G', bound=BaseSeqGame)


class MCTestCaseMixin(Generic[G], ABC):
    @property
    @abstractmethod
    def test_count(self) -> int:
        pass

    def test_monte_carlo(self) -> None:
        for i in range(self.test_count):
            game = self.create_game()

            while game.env.actor is not None:
                self.act(game)
                self.verify(game)

    def verify(self, game: G) -> None:
        if game.is_terminal:
            assert game.env.actor is None
        else:
            assert game.env.actor is not None

    @abstractmethod
    def act(self, game: G) -> None:
        pass

    @abstractmethod
    def create_game(self) -> G:
        pass
