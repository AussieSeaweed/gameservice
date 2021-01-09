from abc import ABC

from gameframe.game import Action


class SequentialAction(Action, ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    @property
    def applicable(self):
        return super().applicable and self.actor is self.game.actor
