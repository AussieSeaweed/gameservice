from gameframe.game import GameFrameException


class InsufficientPlayerCountException(GameFrameException):
    """The number of players are insufficient."""
    pass


class InvalidBlindConfigurationException(GameFrameException):
    """The blind configuration is invalid."""
    pass
