from abc import ABC

from .games import SequentialGame
from ..game import Action


class SequentialAction(Action, ABC):
    """
    This is a class that represents sequential actions.
    """

    def validate(self):
        super().validate()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not a sequential game')
        if self.player is not self.game.player:
            raise ValueError(f'{self.player} is not the player in turn')
