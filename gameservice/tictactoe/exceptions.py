"""
This module defines tic tac toe exceptions in gameservice.
"""
from ..game import GameServiceException


class TicTacToeException(GameServiceException):
    """A base exception class for exceptions related to tic tac toe."""
    pass


class TicTacToeCellException(TicTacToeException):
    """The cell is already occupied."""
    pass
