from abc import ABC, abstractmethod
from time import time
from typing import Generic

from gameframe.game import _G


class GameFrameTestCaseMixin(Generic[_G], ABC):
    MONTE_CARLO_TEST_COUNT: int
    SPEED_TEST_TIME: float

    def test_monte_carlo(self) -> None:
        for _ in range(self.MONTE_CARLO_TEST_COUNT):
            game = self.create_game()

            self.verify(game)

            while not game.terminal:
                self.act(game)
                self.verify(game)

    def test_speed(self) -> None:
        init_time = time()
        count = 0

        while time() - init_time < self.SPEED_TEST_TIME:
            count += 1
            game = self.create_game()

            while not game.terminal:
                self.act(game)

        print(f'{count} {type(self.create_game()).__name__} played in {self.SPEED_TEST_TIME} second.')

    @abstractmethod
    def create_game(self) -> _G:
        ...

    @abstractmethod
    def act(self, game: _G) -> None:
        ...

    @abstractmethod
    def verify(self, game: _G) -> None:
        ...
