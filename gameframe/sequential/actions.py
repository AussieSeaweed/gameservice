from abc import ABC

from gameframe.game import Action
from gameframe.sequential.exceptions import ActorOutOfTurnException


class SequentialAction(Action, ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    def _verify(self):
        super()._verify()

        if self._actor is not self._game.actor:
            raise ActorOutOfTurnException()
