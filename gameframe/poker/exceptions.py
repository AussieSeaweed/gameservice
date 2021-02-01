from gameframe.game import ActionException


class StageException(ActionException):
    pass


class RedundancyException(ActionException):
    pass


class CoveredStackException(ActionException):
    pass


class AmountOutOfBoundsException(ActionException):
    pass
