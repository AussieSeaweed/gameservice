from __future__ import annotations

from typing import TYPE_CHECKING, final

from gameframe.tictactoe.bases import TicTacToeAction
from gameframe.tictactoe.exceptions import CoordinatesOutOfBoundsException, OccupiedCellException
from gameframe.utils import override

if TYPE_CHECKING:
    from gameframe.tictactoe import TicTacToePlayer


@final
class MarkAction(TicTacToeAction):
    """MarkAction is the class for mark actions."""

    def __init__(self, player: TicTacToePlayer, r: int, c: int) -> None:
        super().__init__(player)

        self.__r: int = r
        self.__c: int = c

    @override
    def act(self) -> None:
        super().act()

        self.game.environment._board[self.__r][self.__c] = self.actor

        if self.game.environment._empty_coordinates and self.game.environment._winner is None:
            self.game._actor = next(self.actor)
        else:
            self.game._actor = None

    @override
    def __str__(self) -> str:
        return f'Mark row {self.__r} column {self.__c}'

    @override
    def _verify(self) -> None:
        super()._verify()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise CoordinatesOutOfBoundsException()
        elif self.game.environment.board[self.__r][self.__c] is not None:
            raise OccupiedCellException()
