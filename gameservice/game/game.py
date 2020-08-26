from abc import ABC, abstractmethod

from ..exceptions import InvalidNumPlayersException
from .player import Player, Nature
from .context import Context
from .players import Players


class Game(ABC):
    min_num_players = None
    max_num_players = None

    num_players = None

    player_type = Player
    nature_type = Nature
    context_type = Context

    players_type = Players

    player_actions_type = None
    nature_actions_type = None

    def __init__(self, num_players=None):
        self.num_players = self.num_players or num_players

        if self.num_players is None or not self.min_num_players <= self.num_players <= self.max_num_players:
            raise InvalidNumPlayersException

        self.players = self.players_type(self)
        self.context = self.context_type(self)

    @property
    @abstractmethod
    def terminal(self):
        pass
