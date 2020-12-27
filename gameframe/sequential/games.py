from abc import ABC, abstractmethod

from ..game import Game, E, N, P
from .utils import G


class SequentialGame(Game[G, E, N, P], ABC):
    """
    This is a class that represents sequential games.

    In sequential games, only one player can act at a time. The player in turn can be accessed through the player
    attribute of the SequentialGame instance. The initial_player abstract property should be overridden by the
    subclasses to represent the player who is the first to act. If a sequential game is terminal, its player attribute
    must be set to None to denote such.
    """

    def __init__(self):
        super().__init__()

        self.player = self.initial_player

    @property
    def terminal(self):
        return self.player is None

    @property
    @abstractmethod
    def initial_player(self) -> P:
        """
        :return: the initial player of the sequential game
        """
        pass
