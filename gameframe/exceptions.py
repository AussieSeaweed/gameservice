from abc import ABC


class GameFrameException(Exception, ABC):
    ...


class ActionException(GameFrameException):
    ...


class ParamException(GameFrameException):
    ...
