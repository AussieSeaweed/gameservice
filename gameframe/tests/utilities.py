from abc import ABC, abstractmethod
from typing import Generic

from gameframe.game import _G


class MonteCarloTestCaseMixin(Generic[_G], ABC):
    monte_carlo_test_count: int

    def test_monte_carlo(self) -> None:
        for _ in range(self.monte_carlo_test_count):
            game = self.create_game()

            self.verify(game)

            while not game.is_terminal():
                self.act(game)
                self.verify(game)

    @abstractmethod
    def create_game(self) -> _G:
        pass

    @abstractmethod
    def act(self, game: _G) -> None:
        pass

    @abstractmethod
    def verify(self, game: _G) -> None:
        pass
