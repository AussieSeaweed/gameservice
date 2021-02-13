from gameframe.game import ActionException


class InvalidPlayerException(ActionException):
    pass


class CardCountException(ActionException):
    pass


class BetRaiseAmountException(ActionException):
    pass
