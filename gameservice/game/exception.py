class GameException(Exception):
    """Base exception class for exceptions related to gameservice"""


class GameTerminalException(GameException):
    """Raised when the terminality of the game is invalid"""


class GameInterruptionException(GameException):
    """Raised when the game has been changed when not allowed"""


class GamePlayerException(GameException):
    """Raised when the player of the game is invalid"""


class GameParameterException(GameException):
    """Raised when the parameter of the game is invalid"""


class GameActionException(GameException):
    """Raised when the action of the game is invalid"""


class GameActionArgumentException(GameException):
    """Raised when one or more action arguments are invalid"""
