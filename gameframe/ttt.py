from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from typing import Optional, cast, final, overload

from auxiliary import next_or_none

from gameframe.exceptions import ActionException
from gameframe.seq import SeqGame, _SeqAction


@final
class TTTPlayer:
    """TTTPlayer is the class for tic tac toe players."""

    def __init__(self, game: TTTGame):
        self.__game = game

    def __repr__(self) -> str:
        return 'O' if self.__game.players[0] is self else 'X'

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: The row number of the cell.
        :param c: The column number of the cell.
        :return: None.
        """
        _MarkAction(self.__game, self, r, c).act()

    @overload
    def can_mark(self) -> bool:
        ...

    @overload
    def can_mark(self, r: int, c: int) -> bool:
        ...

    def can_mark(self, r: Optional[int] = None, c: Optional[int] = None) -> bool:
        """Determines if the cell of the board at the coordinates can be marked.

        :param r: The row number of the cell.
        :param c: The column number of the cell.
        :return: True if the cell can be marked, else False.
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
class TTTGame(SeqGame[None, TTTPlayer]):
    """TTTGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        super().__init__(None, players := (TTTPlayer(self), TTTPlayer(self)), players[0])

        self._board: list[list[Optional[TTTPlayer]]] = [[None, None, None],
                                                        [None, None, None],
                                                        [None, None, None]]

    @property
    def board(self) -> Sequence[Sequence[Optional[TTTPlayer]]]:
        """
        :return: The board of this tic tac toe game.
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_coords(self) -> Iterator[tuple[int, int]]:
        """
        :return: The list of the empty coordinates of the board.
        """
        return ((r, c) for r in range(3) for c in range(3) if self._board[r][c] is None)

    @property
    def winner(self) -> Optional[TTTPlayer]:
        """
        :return: The winning player of the tic tac toe game if there is one, else None.
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


class _MarkAction(_SeqAction[TTTGame, TTTPlayer]):
    def __init__(self, game: TTTGame, actor: TTTPlayer, r: int, c: int):
        super().__init__(game, actor)

        self.r, self.c = r, c

    @property
    def next_actor(self) -> Optional[TTTPlayer]:
        if next_or_none(self.game.empty_coords) is not None and self.game.winner is None:
            return self.game.players[self.game.players[0] is self.actor]
        else:
            return None

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.r, int) or not isinstance(self.c, int):
            raise TypeError('The coordinates must be of type int')
        elif not (0 <= self.r < 3 and 0 <= self.c < 3):
            raise ActionException('The coordinates are out of bounds')
        elif self.game._board[self.r][self.c] is not None:
            raise ActionException('The cell is not empty')

    def apply(self) -> None:
        self.game._board[self.r][self.c] = self.actor


def parse_ttt(game: TTTGame, coords: Iterable[Sequence[int]]) -> TTTGame:
    """Parses the coords as mark actions and applies them the supplied tic tac toe game.

    :param game: The tic tac toe game to be applied on.
    :param coords: The coordinates to mark.
    :return: None.
    """
    for r, c in coords:
        cast(TTTPlayer, game._actor).mark(r, c)

    return game
