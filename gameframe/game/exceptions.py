from abc import ABC
from collections.abc import Sequence
from typing import final

__all__: Sequence[str] = ['GameFrameException', 'PlayerTypeMismatchException', 'TerminalityException']


class GameFrameException(Exception, ABC):
    """GameFrameException is the base exception class for all GameFrame exceptions."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)


@final
class PlayerTypeMismatchException(GameFrameException):
    """Natures act chance actions and players act non-chance actions."""
    pass


@final
class TerminalityException(GameFrameException):
    """Action cannot be applied to terminal games."""
    pass
