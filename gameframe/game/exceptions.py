from abc import ABC


class GameFrameException(Exception, ABC):
    """GameFrameException is the base exception class for all GameFrame exceptions."""

    def __init__(self):
        super().__init__(self.__doc__)


class TerminalGameException(GameFrameException):
    """Actions cannot be applied to terminal games."""
    pass
