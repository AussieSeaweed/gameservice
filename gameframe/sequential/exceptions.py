from collections.abc import Sequence
from typing import final

from gameframe.game import GameFrameException

__all__: Sequence[str] = ['ActorOutOfTurnException']


@final
class ActorOutOfTurnException(GameFrameException):
    """The actor is not in turn to act."""
    pass
