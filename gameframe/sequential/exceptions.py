from gameframe.game import GameFrameException


class ActorOutOfTurnException(GameFrameException):
    """The actor is not in turn to act."""
    pass
