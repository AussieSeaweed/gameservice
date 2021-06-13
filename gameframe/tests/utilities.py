from abc import ABC, abstractmethod
from time import time


class GameFrameTestCaseMixin(ABC):
    MONTE_CARLO_TEST_COUNT = None
    SPEED_TEST_TIME = None

    def test_monte_carlo(self):
        for _ in range(self.MONTE_CARLO_TEST_COUNT):
            game = self.create_game()

            self.verify(game)

            while not game.is_terminal():
                self.act(game)
                self.verify(game)

    def test_speed(self):
        init_time = time()
        count = 0

        while time() - init_time < self.SPEED_TEST_TIME:
            count += 1
            game = self.create_game()

            while not game.is_terminal():
                self.act(game)

        print(f'{count} {type(self.create_game()).__name__}(s) played in {self.SPEED_TEST_TIME} second(s).')

    @abstractmethod
    def create_game(self):
        ...

    @abstractmethod
    def act(self, game):
        ...

    @abstractmethod
    def verify(self, game):
        ...
