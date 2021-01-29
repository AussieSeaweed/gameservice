from abc import ABC


class GameFrameException(BaseException, ABC):
    """GameFrameException is the base exception class for all GameFrame
    exceptions.
    """

    def __init__(self) -> None:
        super().__init__(self.__doc__)


class ActionException(GameFrameException):
    """The action cannot be applied."""
    pass
