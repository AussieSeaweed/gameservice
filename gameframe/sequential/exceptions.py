from typing import final

from gameframe.game import GameFrameException


@final
class ActorOutOfTurnException(GameFrameException):
    pass
