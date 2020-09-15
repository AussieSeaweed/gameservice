from abc import ABC, abstractmethod


class Game(ABC):
    player_type = None
    nature_type = None
    context_type = None

    num_players = None
    players_type = None

    player_actions_type = None
    nature_actions_type = None

    def __init__(self):
        self.players = self.players_type(self)
        self.context = self.context_type(self)

    @property
    @abstractmethod
    def terminal(self):
        pass
