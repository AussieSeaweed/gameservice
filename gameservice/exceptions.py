class GameServiceException(Exception):
    """Base exception class for exceptions related to gameservice"""


class GameTerminalException(GameServiceException):
    """Raised when the terminality of the game is invalid"""


class GameInterruptedException(GameServiceException):
    """Raised when the terminality of the game is invalid"""


class GamePlayerException(GameServiceException):
    """Raised when the player is invalid"""
