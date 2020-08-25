class GameServiceException(Exception):
    """Base class for other exceptions"""


class TerminalGameException(GameServiceException):
    """Raised when the game is terminal"""


class PlayerOutOfTurnException(GameServiceException):
    """Raised when the player acts out of turn"""


class InvalidActionArgumentException(GameServiceException):
    """Raised when an argument to an action is invalid"""
