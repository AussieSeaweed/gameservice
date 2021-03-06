from abc import ABC


class GameFrameException(Exception, ABC):
    """GameFrameException is the base exception class for all GameFrame exceptions."""
    pass


class ActionException(GameFrameException):
    """ActionException is the exception class for action exceptions."""
    pass


class ParamException(GameFrameException):
    """ParamException is the exception class for parameter exceptions."""
    pass
