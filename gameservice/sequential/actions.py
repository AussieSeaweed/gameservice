from abc import ABC

from ..exceptions import PlayerOutOfTurnException
from ..game.actions import Action


class SequentialAction(Action, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if game.player is not player:
            raise PlayerOutOfTurnException(f"{player} is not allowed to act now")
