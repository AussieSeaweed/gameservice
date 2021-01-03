from typing import final

from gameframe.game import GameFrameException


@final
class ActorOutOfTurnException(GameFrameException):
    """The actor is not in turn to act."""
    pass
