from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from random import choice
from typing import Optional, cast, final, overload

from auxiliary import next_or_none

from gameframe.exceptions import GameFrameValueError
from gameframe.sequential import SequentialActor, SequentialGame, _SequentialAction


@final
class TicTacToe(SequentialGame['TicTacToe', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToe is the class for tic tac toe games."""

    def __init__(self) -> None:
        self._board: list[list[Optional[TicTacToePlayer]]] = [[None, None, None],
                                                              [None, None, None],
                                                              [None, None, None]]

        self._nature = TicTacToeNature(self)
        self._players = [TicTacToePlayer(self), TicTacToePlayer(self)]
        self._actor = self.players[0]

    @property
    def board(self) -> Sequence[Sequence[Optional[TicTacToePlayer]]]:
        """
        :return: The board of this tic tac toe game.
        """
        return self._board

    @property
    def empty_coordinates(self) -> Iterator[tuple[int, int]]:
        """
        :return: The list of the empty coordinates of the board.
        """
        return ((r, c) for r in range(3) for c in range(3) if self.board[r][c] is None)

    @property
    def winner(self) -> Optional[TicTacToePlayer]:
        """
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
class TicTacToeNature(SequentialActor[TicTacToe, 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeNature is the class for tic tac toe natures."""

    def __init__(self, game: TicTacToe):
        self._game = game


@final
class TicTacToePlayer(SequentialActor[TicTacToe, TicTacToeNature, 'TicTacToePlayer']):
    """TicTacToePlayer is the class for tic tac toe players."""

    def __init__(self, game: TicTacToe):
        self._game = game

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
        _MarkAction(self, r, c).act()

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
        return _MarkAction(self, r, c).can_act()

    def __repr__(self) -> str:
        return 'O' if self.game.players[0] is self else 'X'


class _MarkAction(_SequentialAction[TicTacToePlayer]):
    def __init__(self, actor: TicTacToePlayer, r: Optional[int] = None, c: Optional[int] = None):
        self.r, self.c = r, c
        self.actor = actor

    def verify(self) -> None:
        super().verify()

        if self.r is not None and self.c is not None:
            if not (0 <= self.r < 3 and 0 <= self.c < 3):
                raise GameFrameValueError('The coordinates must be within bounds (from 0 to 3 inclusive)')
            elif self.actor.game._board[self.r][self.c] is not None:
                raise GameFrameValueError('The cell to be marked must be empty')

    def apply(self) -> None:
        game = self.actor.game

        if self.r is not None and self.c is not None:
            r, c = self.r, self.c
        else:
            r, c = choice(tuple(game.empty_coordinates))

        game._board[r][c] = self.actor

        if next_or_none(game.empty_coordinates) is not None and game.winner is None:
            game._actor = game.players[game.players[0] is self.actor]
        else:
            game._actor = None


def parse_tic_tac_toe(game: TicTacToe, coords: Iterable[Sequence[int]]) -> TicTacToe:
    """Parses the coords as mark actions and applies them the supplied tic tac toe game.

    :param game: The tic tac toe game to be applied on.
    :param coords: The coordinates to mark.
    :return: None.
    """
    for r, c in coords:
        cast(TicTacToePlayer, game.actor).mark(r, c)

    return game
