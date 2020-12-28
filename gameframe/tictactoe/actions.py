from __future__ import annotations

from typing import TYPE_CHECKING

from ..sequential import SequentialAction

if TYPE_CHECKING:
    from . import TicTacToePlayer


class MarkAction(SequentialAction['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """MarkAction is the class for mark actions."""

    def __init__(self, player: TicTacToePlayer, r: int, c: int):
        super().__init__(player)

        self.__r: int = r
        self.__c: int = c

    def act(self) -> None:
        super().act()

        self.game.environment.board[self.__r][self.__c]: TicTacToePlayer = self.player

        if self.game.environment._empty_coordinates and self.game.environment._winner is None:
            self.game.player = next(self.player)
        else:
            self.game.player = None

    @property
    def chance(self) -> bool:
        return False

    @property
    def public(self) -> bool:
        return True

    def __str__(self) -> str:
        return f'Mark row {self.__r} column {self.__c}'

    def _verify(self) -> None:
        super()._verify()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise ValueError('The cell coordinates are out of range')
        elif self.game.environment.board[self.__r][self.__c] is not None:
            raise ValueError('The cell is already occupied')
