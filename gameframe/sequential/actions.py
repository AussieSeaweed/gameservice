from abc import ABC

from .games import SequentialGame
from ..game import Action, E, N, P
from .utils import G


class SequentialAction(Action[G, E, N, P], ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    def verify(self) -> None:
        """
        :return: None
        :raise TypeError: if the game is not an instance of SequentialGame
        """
        super().verify()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not an instance of SequentialGame')
        if self.player is not self.game.player:
            raise ValueError('The acting player is not in turn to act')
