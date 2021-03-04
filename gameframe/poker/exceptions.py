from gameframe.exceptions import ActionException


class InvalidPlayerException(ActionException):
    ...


class CardCountException(ActionException):
    ...


class BetRaiseAmountException(ActionException):
    ...
