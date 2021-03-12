from abc import ABC


class GameFrameException(Exception, ABC):
    """GameFrameException is the base exception class for all GameFrame exceptions."""
    pass


class ActionException(GameFrameException):
    """ActionException is the exception class for action exceptions."""
    pass


class ParameterException(GameFrameException):
    """ParameterException is the exception class raised when the game parameter is invalid."""
    pass
