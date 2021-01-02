from typing import final

from gameframe.game import GameFrameException


@final
class OccupiedCellException(GameFrameException):
    pass


@final
class CoordinatesOutOfBoundsException(GameFrameException):
    pass
