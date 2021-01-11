from abc import ABC

from gameframe.game import Action


class SequentialAction(Action, ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    @property
    def is_applicable(self):
        return super().is_applicable and self.actor is self.game.actor
