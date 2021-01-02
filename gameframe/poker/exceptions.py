from typing import final

from gameframe.game import GameFrameException


@final
class InsufficientPlayerCountException(GameFrameException):
    """The number of players are insufficient."""
    pass


@final
class InvalidBlindConfigurationException(GameFrameException):
    """The blind configurations are invalid."""
    pass


@final
class FutileActionException(GameFrameException):
    """The actions cannot be applied because it is futile."""
    pass


@final
class AmountOutOfBoundsException(GameFrameException):
    """The amount is out of the allowed range."""
    pass
