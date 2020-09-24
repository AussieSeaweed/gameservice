from abc import ABC, abstractmethod


class Game(ABC):
    player_type = None
    nature_type = None
    context_type = None

    num_players = None
    playerset_type = None

    player_actionset_type = None
    nature_actionset_type = None

    def __init__(self):
        self.players = self.playerset_type(self)
        self.context = self.context_type(self)

    @property
    @abstractmethod
    def terminal(self):
        pass
