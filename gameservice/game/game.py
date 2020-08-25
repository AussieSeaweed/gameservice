from abc import ABC, abstractmethod

from .players import Players


class Game(ABC):
    player_type = None
    nature_type = None
    context_type = None
    players_type = Players

    def __init__(self):
        self.__players = self.players_type(self)
        self.__context = self.context_type()

    @property
    def players(self):
        return self.__players

    @property
    def context(self):
        return self.__context

    @property
    @abstractmethod
    def num_players(self):
        pass
