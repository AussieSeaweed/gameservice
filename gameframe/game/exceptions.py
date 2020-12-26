"""
This module defines exceptions in gameframe.
"""


class GameException(Exception):
    """A base exception class for exceptions related to gameframe."""
    pass


class ActionArgumentException(GameException):
    """One or more invalid arguments are supplied to the action."""
    pass


class ActionException(GameException):
    """The action is invalid."""
    pass


class ParameterException(GameException):
    """One or more invalid parameters are supplied to the game."""
    pass


class PlayerException(GameException):
    """The player cannot perform the action."""
    pass


class TerminalException(GameException):
    """The terminality of the game is invalid."""
    pass


class TypeException(GameException):
    """The type of the game is invalid."""
    pass
