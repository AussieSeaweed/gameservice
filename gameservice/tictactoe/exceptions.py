"""
This module defines tic tac toe exceptions in gameservice.
"""
from ..game import GameServiceException


class TTTException(GameServiceException):
    """A base exception class for exceptions related to tic tac toe."""
    pass


class TTTCellException(TTTException):
    """The cell is already occupied."""
    pass
