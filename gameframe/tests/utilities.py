from abc import ABC, abstractmethod
from time import time
from typing import Generic

from gameframe.game import _G


class GameFrameTestCaseMixin(Generic[_G], ABC):
    monte_carlo_test_count: int
    speed_test_time: float

    def test_monte_carlo(self) -> None:
        for _ in range(self.monte_carlo_test_count):
            game = self.create_game()

            self.verify(game)

            while not game.terminal:
                self.act(game)
                self.verify(game)

    def test_speed(self) -> None:
        init_time = time()
        count = 0

        while time() - init_time < self.speed_test_time:
            count += 1
            game = self.create_game()

            while not game.terminal:
                self.act(game)

        print(f'{count} {type(self.create_game()).__name__} played in {self.speed_test_time} second.')

    @abstractmethod
    def create_game(self) -> _G:
        pass

    @abstractmethod
    def act(self, game: _G) -> None:
        pass

    @abstractmethod
    def verify(self, game: _G) -> None:
        pass
