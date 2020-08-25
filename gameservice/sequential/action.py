from abc import ABC

from ..game.action import Action
from ..exceptions import PlayerOutOfTurnException


class SequentialAction(Action, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if game.player is not player:
            raise PlayerOutOfTurnException
