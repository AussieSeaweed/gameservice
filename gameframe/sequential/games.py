from abc import ABC, abstractmethod

from ..game import Game


class SequentialGame(Game, ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one player can act at a time. The player in turn can be accessed through the player
    attribute of the SequentialGame instance. The initial_player abstract property should be overridden by the
    subclasses to represent the player who is the first to act. If a sequential game is terminal, its player attribute
    must be set to None to denote such.
    """

    def __init__(self):
        super().__init__()

        self._player = self._initial_player

    @property
    def player(self):
        """
        :return: the player in turn to act of the sequential game
        """
        return self._player

    @property
    def terminal(self):
        return self.player is None

    @property
    def _information(self):
        return {
            **super()._information,
            'player': self.player,
        }

    @property
    @abstractmethod
    def _initial_player(self):
        pass
