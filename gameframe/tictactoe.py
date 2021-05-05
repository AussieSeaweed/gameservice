from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from typing import Optional, cast, final

from auxiliary import next_or_none

from gameframe.exceptions import GameFrameValueError
from gameframe.sequential import SequentialGame, SequentialActor


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
    def empty_coords(self) -> Iterator[tuple[int, int]]:
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

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: The row number of the cell.
        :param c: The column number of the cell.
        :return: None.
        """
        if not (0 <= r < 3 and 0 <= c < 3):
            raise GameFrameValueError('The coordinates are out of bounds')
        elif self.game.board[r][c] is not None:
            raise GameFrameValueError('The cell is not empty')

        self.game._board[r][c] = self

        if next_or_none(self.game.empty_coords) is not None and self.game.winner is None:
            self.game._actor = self.game.players[self.game.players[0] is self]
        else:
            self.game._actor = None

    def __repr__(self) -> str:
        return 'O' if self.game.players[0] is self else 'X'


def parse_tic_tac_toe(game: TicTacToe, coords: Iterable[Sequence[int]]) -> TicTacToe:
    """Parses the coords as mark actions and applies them the supplied tic tac toe game.

    :param game: The tic tac toe game to be applied on.
    :param coords: The coordinates to mark.
    :return: None.
    """
    for r, c in coords:
        cast(TicTacToePlayer, game.actor).mark(r, c)

    return game
