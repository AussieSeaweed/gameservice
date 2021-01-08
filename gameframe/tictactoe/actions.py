from abc import ABC

from gameframe.sequential import SequentialAction
from gameframe.tictactoe.exceptions import CoordinatesOutOfBoundsException, OccupiedCellException


class TicTacToeAction(SequentialAction, ABC):
    """TicTacToeAction is the abstract base class for all tic tac toe actions"""

    @property
    def public(self):
        return True


class MarkAction(TicTacToeAction):
    """MarkAction is the class for mark actions."""

    def __init__(self, player, r, c):
        super().__init__(player)

        self.__r = r
        self.__c = c

    def __str__(self):
        return f'Mark row {self.__r} column {self.__c}'

    def act(self):
        super().act()

        self._game.environment._board[self.__r][self.__c] = self._actor

        if self._game.environment._empty_coordinates and self._game.environment._winner is None:
            self._game._actor = next(self._actor)
        else:
            self._game._actor = None

    def _verify(self):
        super()._verify()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise CoordinatesOutOfBoundsException()
        elif self._game.environment.board[self.__r][self.__c] is not None:
            raise OccupiedCellException()
