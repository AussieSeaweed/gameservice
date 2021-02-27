from __future__ import annotations

from collections import Iterable, Iterator, Sequence
from typing import Optional, cast, final, overload

from auxiliary.utils import next_or_none

from gameframe.exceptions import ActionException
from gameframe.sequential import SequentialGame, _SequentialAction


@final
class TTTPlayer:
    """TTTPlayer is the class for tic tac toe players."""

    def __init__(self, game: TTTGame):
        self.__game = game

    def __repr__(self) -> str:
        return 'O' if self.__game.players[0] is self else 'X'

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        """
        _MarkAction(self.__game, self, r, c).act()

    @overload
    def can_mark(self) -> bool: ...

    @overload
    def can_mark(self, r: int, c: int) -> bool: ...

    def can_mark(self, r: Optional[int] = None, c: Optional[int] = None) -> bool:
        """Determines if the cell of the board at the coordinates can be marked.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: True if the cell can be marked, else False
        """
        try:
            if r is None or c is None:
                _MarkAction(self.__game, self, *(next(self.__game.empty_coords))).verify()
            else:
                _MarkAction(self.__game, self, r, c).verify()
        except ActionException:
            return False
        else:
            return True


@final
class TTTGame(SequentialGame[None, TTTPlayer]):
    """TTTGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        players = TTTPlayer(self), TTTPlayer(self)

        super().__init__(None, players, players[0])

        self._board: list[list[Optional[TTTPlayer]]] = [[None, None, None],
                                                        [None, None, None],
                                                        [None, None, None]]

    @property
    def board(self) -> Sequence[Sequence[Optional[TTTPlayer]]]:
        """
        :return: the board of this tic tac toe game
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_coords(self) -> Iterator[tuple[int, int]]:
        """
        :return: the list of the empty coordinates of the board
        """
        return ((r, c) for r in range(3) for c in range(3) if self._board[r][c] is None)

    @property
    def winner(self) -> Optional[TTTPlayer]:
        """
        :return: the winning player of the tic tac toe game if there is one, else None
        """
        for i in range(3):
            if self._board[i][0] is self._board[i][1] is self._board[i][2] is not None:
                return self._board[i][0]
            elif self._board[0][i] is self._board[1][i] is self._board[2][i] is not None:
                return self._board[0][i]

        if self._board[1][1] is not None and (self._board[0][0] is self._board[1][1] is self._board[2][2]
                                              or self._board[0][2] is self._board[1][1] is self._board[2][0]):
            return self._board[1][1]

        return None


class _MarkAction(_SequentialAction[TTTGame, TTTPlayer]):
    def __init__(self, game: TTTGame, actor: TTTPlayer, r: int, c: int):
        super().__init__(game, actor)

        self.r, self.c = r, c

    @property
    def next_actor(self) -> Optional[TTTPlayer]:
        if next_or_none(self.game.empty_coords) is not None and self.game.winner is None:
            return self.game.players[not self.game.players.index(self.actor)]
        else:
            return None

    def apply(self) -> None:
        self.game._board[self.r][self.c] = self.actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.r, int) or not isinstance(self.c, int):
            raise TypeError('The coordinates must be of type int')
        elif not (0 <= self.r < 3 and 0 <= self.c < 3):
            raise ActionException('The coordinates are out of bounds')
        elif self.game._board[self.r][self.c] is not None:
            raise ActionException('The cell is not empty')


def parse_ttt(game: TTTGame, coords: Iterable[Sequence[int]]) -> None:
    """Parses the coords as mark actions and applies them the supplied tic tac toe game.

    :param game: the tic tac toe game to be applied on
    :param coords: the coordinates to mark
    :return: None
    """
    for r, c in coords:
        cast(TTTPlayer, game.actor).mark(r, c)
