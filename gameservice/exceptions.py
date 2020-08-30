class GameServiceException(Exception):
    """Base class for other exceptions"""


class InvalidNumPlayersException(GameServiceException):
    """Raised when the number of players is invalid"""


class TerminalGameException(GameServiceException):
    """Raised when the game is terminal"""


class PlayerOutOfTurnException(GameServiceException):
    """Raised when the player acts out of turn"""


class InvalidActionException(GameServiceException):
    """Raised when an action is invalid"""


class InvalidActionArgumentException(GameServiceException):
    """Raised when an argument to an action is invalid"""


class NatureException(GameServiceException):
    """Raised when the nature is absent"""
