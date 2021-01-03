from typing import final


class GameFrameException(Exception):
    """GameFrameException is the base exception class for all GameFrame exceptions."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)


@final
class TerminalityException(GameFrameException):
    """Action cannot be applied to terminal games."""
    pass


@final
class PlayerTypeMismatchException(GameFrameException):
    """Natures act chance actions and players act non-chance actions."""
    pass
