from gameframe.game import GameFrameException


class BlindException(GameFrameException):
    """The blind configuration is invalid."""
    pass


class PlayerCountException(GameFrameException):
    """The number of players are insufficient."""
    pass


class IllegalStateException(GameFrameException):
    """The state is illegal."""
    pass
