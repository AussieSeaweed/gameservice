from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from random import choice
from typing import Optional, cast, final, overload

from auxiliary import next_or_none

from gameframe.exceptions import GameFrameError
from gameframe.game import Actor, BaseActor
from gameframe.sequential import SequentialGame, _SequentialAction


@final
class TicTacToe(SequentialGame[BaseActor, 'TicTacToePlayer']):
    """TicTacToe is the class for tic tac toe games."""

    def __init__(self) -> None:
        super().__init__(0, Actor(self), (TicTacToePlayer(self), TicTacToePlayer(self)))

        self._board: list[list[Optional[TicTacToePlayer]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    @property
    def board(self) -> Sequence[Sequence[Optional[TicTacToePlayer]]]:
        """Returns the board of this tic tac toe game.

        :return: The board of this tic tac toe game.
        """
        return self._board

    @property
    def empty_coordinates(self) -> Iterator[tuple[int, int]]:
        """Returns the empty coordinates of the board of this tic tac toe game.

        :return: The list of the empty coordinates of the board.
        """
        return ((r, c) for r in range(3) for c in range(3) if self.board[r][c] is None)

    @property
    def winner(self) -> Optional[TicTacToePlayer]:
        """Returns the winner of this tic tac toe game.

        :return: The winning player of the tic tac toe game if there is one, else None.
        """
        for i in range(3):
            if self.board[i][0] is self.board[i][1] is self.board[i][2] is not None:
                return self.board[i][0]
            elif self.board[0][i] is self.board[1][i] is self.board[2][i] is not None:
                return self.board[0][i]

        if self.board[1][1] is not None and (self.board[0][0] is self.board[1][1] is self.board[2][2]
                                             or self.board[0][2] is self.board[1][1] is self.board[2][0]):
            return self.board[1][1]

        return None


@final
class TicTacToePlayer(Actor[TicTacToe]):
    """TicTacToePlayer is the class for tic tac toe players."""

    def __repr__(self) -> str:
        return 'O' if self.game.players[0] is self else 'X'

    @overload
    def mark(self) -> None: ...

    @overload
    def mark(self, r: int, c: int) -> None: ...

    def mark(self, r: Optional[int] = None, c: Optional[int] = None) -> None:
        """Marks the cell of the board at the optionally specified coordinates.

        If the row and column numbers are not supplied, they are randomly determined among empty cells.

        :param r: The row number of the cell.
        :param c: The column number of the cell.
        :return: None.
        """
        _MarkAction(r, c, self).act()

    @overload
    def can_mark(self) -> bool: ...

    @overload
    def can_mark(self, r: int, c: int) -> bool: ...

    def can_mark(self, r: Optional[int] = None, c: Optional[int] = None) -> bool:
        """Determines if the cell of the board at the coordinates can be marked.

        :param r: The optional row number of the cell.
        :param c: The optional column number of the cell.
        :return: True if the cell can be marked, else False.
        """
        return _MarkAction(r, c, self).can_act()


class _MarkAction(_SequentialAction[TicTacToe, TicTacToePlayer]):
    def __init__(self, r: Optional[int], c: Optional[int], actor: TicTacToePlayer):
        super().__init__(actor)

        self.r, self.c = r, c

    def verify(self) -> None:
        super().verify()

        if self.r is not None and self.c is not None:
            if not (0 <= self.r < 3 and 0 <= self.c < 3):
                raise GameFrameError('The coordinates must be within bounds (from 0 to 3 inclusive)')
            elif self.game.board[self.r][self.c] is not None:
                raise GameFrameError('The cell to be marked must be empty')

    def apply(self) -> None:
        super().apply()

        if self.r is None or self.c is None:
            self.r, self.c = choice(tuple(self.game.empty_coordinates))

        self.game._board[self.r][self.c] = self.actor

        if next_or_none(self.game.empty_coordinates) is not None and self.game.winner is None:
            self.game._actor = self.game.players[self.game.players[0] is self.actor]
        else:
            self.game._actor = None


def parse_tic_tac_toe(game: TicTacToe, coords: Iterable[Sequence[int]]) -> TicTacToe:
    """Parses the coords as mark actions and applies them the supplied tic tac toe game.

    :param game: The tic tac toe game to be applied on.
    :param coords: The coordinates to mark.
    :return: None.
    """
    for r, c in coords:
        cast(TicTacToePlayer, game.actor).mark(r, c)

    return game
