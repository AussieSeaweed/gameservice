from typing import final

from gameframe.game import GameFrameException


@final
class CoordinatesOutOfBoundsException(GameFrameException):
    """The cell coordinates are out of range."""
    pass


@final
class OccupiedCellException(GameFrameException):
    """The cell is already occupied."""
    pass
