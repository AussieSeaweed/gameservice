from abc import ABC, abstractmethod
from time import time


class GameFrameTestCaseMixin(ABC):
    @property
    def test_time(self):
        return 1

    @property
    def game_name(self):
        return type(self.create_game()).__name__

    def test_monte_carlo(self):
        init_time = time()

        while time() - init_time < self.test_time:
            game = self.create_game()

            self.verify(game)

            while not game.is_terminal():
                self.act(game)
                self.verify(game)

    def test_speed(self):
        init_time = time()
        count = 0

        while time() - init_time < self.test_time:
            count += 1
            game = self.create_game()

            while not game.is_terminal():
                self.act(game)

        print(f'{count} {self.game_name}(s) played in {self.test_time} second(s).')

    @abstractmethod
    def create_game(self):
        ...

    @abstractmethod
    def act(self, game):
        ...

    @abstractmethod
    def verify(self, game):
        ...
