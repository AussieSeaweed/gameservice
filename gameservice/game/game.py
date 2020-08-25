from abc import ABC, abstractmethod

from .player import Player, Nature
from .context import Context
from .players import Players


class Game(ABC):
    num_players = None

    player_type = Player
    nature_type = Nature
    context_type = Context

    players_type = Players
    actions_type = None

    def __init__(self):
        self.__players = self.players_type(self)
        self.__context = self.context_type(self)

    @property
    def players(self):
        return self.__players

    @property
    def context(self):
        return self.__context

    @property
    @abstractmethod
    def terminal(self):
        pass
