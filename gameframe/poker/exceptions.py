from gameframe.game import GameFrameException


class PlayerCountException(GameFrameException):
    """The number of players are insufficient."""
    pass


class BlindConfigException(GameFrameException):
    """The blind configuration is invalid."""
    pass


class IllegalStateException(GameFrameException):
    """The program is in an invalid state."""
    pass
