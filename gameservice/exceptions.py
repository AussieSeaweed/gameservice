class GameException(Exception):
    """Base class for other exceptions"""


class GameTerminalException(GameException):
    """Raised when the game is terminal"""


class GameConfigException(GameException):
    """Raised when the game config is invalid"""


class PlayerException(GameException):
    """Base class for player exceptions"""


class PlayerNumException(PlayerException):
    """Raised when the number of players is invalid"""


class PlayerNotFoundException(PlayerException):
    """Raised when requested player is not found"""


class PlayerOutOfTurnException(PlayerException):
    """Raised when the player acts out of turn"""


class PlayerTypeException(PlayerException):
    """Raised when the player or nature is not permitted"""


class ActionException(GameException):
    """Base class for action exceptions"""


class ActionNotFoundException(ActionException):
    """Raised when an action is not found"""


class ActionArgumentException(ActionException):
    """Raised when an argument to an action is invalid"""
