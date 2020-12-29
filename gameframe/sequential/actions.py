from abc import ABC

from .games import SequentialGame
from ..game import Action


class SequentialAction(Action, ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    def _verify(self):
        super()._verify()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not an instance of SequentialGame')
        if self.player is not self.game.player:
            raise ValueError('The acting player is not in turn to act')
