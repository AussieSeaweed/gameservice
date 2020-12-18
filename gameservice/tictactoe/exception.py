from ..game import GameException


class TTTException(GameException):
    """Base exception class for exceptions related to TTTGame."""
    pass


class TTTCellException(GameException):
    """The cell is already occupied."""
    pass
