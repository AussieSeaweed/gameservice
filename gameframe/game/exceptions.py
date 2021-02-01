from abc import ABC


class GameFrameException(Exception, ABC):
    pass


class ParamException(GameFrameException):
    pass


class ActionException(GameFrameException):
    pass
