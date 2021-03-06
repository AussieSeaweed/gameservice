from gameframe.exceptions import GameFrameException, ActionException


class ParamException(GameFrameException):
    """ParamException is the exception class for parameter exceptions."""
    pass


class PlayerException(ActionException):
    """PlayerException is the exception class raised when the player is invalid."""
    pass


class CardCountException(ActionException):
    """CardCountException is the exception class raised when the number of cards is invalid."""
    pass


class BetRaiseAmountException(ActionException):
    """BetRaiseAmountException is the exception class raised when the bet/raise amount is invalid."""
    pass
