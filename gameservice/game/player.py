from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        return self.__game

    @property
    def nature(self):
        return self is self.game.nature

    @property
    def index(self):
        return None if self.nature else self.game.players.index(self)

    @property
    @abstractmethod
    def payoff(self):
        pass

    @property
    @abstractmethod
    def actions(self):
        pass

    @property
    @abstractmethod
    def info_set(self):
        pass

    def __next__(self):
        return self.game.nature if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        return f'Player {self.index}'


class Nature(Player, ABC):
    @property
    def payoff(self):
        return -sum(player.payoff for player in self.game.players)

    def __str__(self):
        return 'Nature'
