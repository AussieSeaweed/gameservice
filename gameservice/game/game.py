from abc import ABC, abstractmethod

from .context import Context
from .player import Player, Nature
from .players import Players


class Game(ABC):
    player_type = Player
    nature_type = Nature
    context_type = Context

    players_type = Players

    player_actions_type = None
    nature_actions_type = None

    def __init__(self):
        self.players = self._create_players()
        self.context = self._create_context()

    def _create_players(self):
        return self.players_type(self)

    def _create_context(self):
        return self.context_type(self)

    @property
    @abstractmethod
    def terminal(self):
        pass
