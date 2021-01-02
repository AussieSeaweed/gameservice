from typing import final

from gameframe.game import GameFrameException


@final
class InsufficientPlayerCountException(GameFrameException):
    pass


@final
class InvalidBlindConfigurationException(GameFrameException):
    pass


@final
class FutileActionException(GameFrameException):
    pass


@final
class AmountOutOfBoundsException(GameFrameException):
    pass
