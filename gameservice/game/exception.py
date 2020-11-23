class GameException(Exception):
    """Base exception class for exceptions related to gameservice"""
    pass


class GameTerminalException(GameException):
    """The terminality of the game is invalid"""
    pass


class GameInterruptionException(GameException):
    """The game has already been modified"""
    pass


class GamePlayerException(GameException):
    """The player cannot perform the action"""
    pass


class GameParameterException(GameException):
    """One or more invalid parameters are supplied to the game"""
    pass


class GameActionException(GameException):
    """The action is invalid"""
    pass


class GameActionArgumentException(GameException):
    """One or more invalid arguments are supplied to the action"""
    pass
