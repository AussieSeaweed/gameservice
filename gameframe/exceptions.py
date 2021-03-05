from abc import ABC


class GameFrameException(Exception, ABC):
    pass


class ActionException(GameFrameException):
    pass


class ParamException(GameFrameException):
    pass
