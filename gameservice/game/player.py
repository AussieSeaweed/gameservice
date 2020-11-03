from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, game, index):
        self.__game = game
        self.__index = index

    @property
    def game(self):
        return self.__game

    @property
    def index(self):
        return self.__index

    @property
    def nature(self):
        return self.index is None

    @property
    @abstractmethod
    def payoff(self):
        pass

    @property
    @abstractmethod
    def actions(self):
        pass

    def __next__(self):
        return self.game.nature if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]


class Nature(Player, ABC):
    def __init__(self, game):
        super().__init__(game, None)

    @property
    def payoff(self):
        return -sum(player.payoff for player in self.game.players)
