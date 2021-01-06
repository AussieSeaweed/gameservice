from collections.abc import Sequence
from typing import final

from gameframe.game import GameFrameException

__all__: Sequence[str] = ['AmountOutOfBoundsException', 'FutileActionException', 'InsufficientPlayerCountException',
                          'InvalidBlindConfigurationException', 'InvalidRoundException', 'UnavailableActionException']


@final
class AmountOutOfBoundsException(GameFrameException):
    """The amount is out of the allowed range."""
    pass


@final
class FutileActionException(GameFrameException):
    """The actions cannot be applied because it is futile."""
    pass


@final
class InsufficientPlayerCountException(GameFrameException):
    """The number of players are insufficient."""
    pass


@final
class InvalidBlindConfigurationException(GameFrameException):
    """The blind configurations are invalid."""
    pass


@final
class InvalidRoundException(GameFrameException):
    """The action is not relevant with this round."""
    pass


@final
class UnavailableActionException(GameFrameException):
    """The action is unavailable."""
    pass
