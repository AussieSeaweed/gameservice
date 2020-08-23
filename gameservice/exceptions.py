class GameServiceException(Exception):
    """Base class for other exceptions"""


class InvalidNumPlayersException(GameServiceException):
    """Raised when the number of players is invalid"""


class InvalidActionException(GameServiceException):
    """Raised when the requested action is invalid"""


class InvalidActionArgumentException(GameServiceException):
    """Raised when at least one provided action argument is invalid"""


class TerminalError(GameServiceException):
    """Raised when the game is terminal"""
