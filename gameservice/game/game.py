from abc import ABC, abstractmethod


class Game(ABC):
    labels = None
    num_players = None

    context_type = None

    nature_type = None
    player_type = None
    playerset_type = None

    nature_actionset_type = None
    player_actionset_type = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.context = self.context_type(self)
        self.players = self.playerset_type(self)

    @property
    @abstractmethod
    def terminal(self):
        pass
