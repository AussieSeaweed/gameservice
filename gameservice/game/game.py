from abc import ABC, abstractmethod


class Game(ABC):
    label = "Game"
    labels = None

    player_type = None
    nature_type = None
    context_type = None

    num_players = None
    playerset_type = None

    player_actionset_type = None
    nature_actionset_type = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.players = self.playerset_type(self)
        self.context = self.context_type(self)

    @property
    @abstractmethod
    def terminal(self):
        pass
