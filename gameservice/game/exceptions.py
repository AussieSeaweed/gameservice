"""
This module defines exceptions in gameservice.
"""


class GameServiceException(Exception):
    """Base exception class for exceptions related to gameservice."""
    pass


class ActionArgumentException(GameServiceException):
    """One or more invalid arguments are supplied to the action."""
    pass


class ActionException(GameServiceException):
    """The action is invalid."""
    pass


class ParameterException(GameServiceException):
    """One or more invalid parameters are supplied to the game."""
    pass


class PlayerException(GameServiceException):
    """The player cannot perform the action."""
    pass


class TerminalException(GameServiceException):
    """The terminality of the game is invalid."""
    pass


class TypeException(GameServiceException):
    """The type of the game is invalid."""
    pass
