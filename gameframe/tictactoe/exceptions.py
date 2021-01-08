from gameframe.game import GameFrameException


class CoordinatesOutOfBoundsException(GameFrameException):
    """The cell coordinates are out of range."""
    pass


class OccupiedCellException(GameFrameException):
    """The cell is already occupied."""
    pass
