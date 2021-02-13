from gameframe.game import ActionException


class MuckedPlayerException(ActionException):
    pass


class CardCountException(ActionException):
    pass


class BetRaiseAmountException(ActionException):
    pass
