from abc import ABC

from .games import SequentialGame
from .utils import G
from ..game import Action, E, N, P


class SequentialAction(Action[G, E, N, P], ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    def _verify(self) -> None:
        super()._verify()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not an instance of SequentialGame')
        if self.player is not self.game.player:
            raise ValueError('The acting player is not in turn to act')
