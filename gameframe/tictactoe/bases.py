from __future__ import annotations

from collections import Sequence
from typing import Optional, final

from gameframe.game import ActionException
from gameframe.game.generics import Actor
from gameframe.sequential.generics import SeqAction, SeqGame


@final
class TTTGame(SeqGame[Actor['TTTGame'], 'TTTPlayer']):
    """TTTGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        nature = Actor(self)
        players = TTTPlayer(self), TTTPlayer(self)
        actor = players[0]

        super().__init__(nature, players, actor)

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
    def empty_coords(self) -> Sequence[Sequence[int]]:
        """
        :return: the list of empty coordinates of the board
        """
        return [[r, c] for r in range(3) for c in range(3) if self._board[r][c] is None]

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


@final
class TTTPlayer(Actor[TTTGame]):
    """TTTPlayer is the class for tic tac toe players."""

    def __repr__(self) -> str:
        return 'O' if self.game.players[0] is self else 'X'

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        """
        MarkAction(self.game, self, r, c).act()

    def can_mark(self, r: int, c: int) -> bool:
        """Determines if the cell of the board at the coordinates can be marked.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: True if the cell can be marked, else False
        """
        try:
            MarkAction(self.game, self, r, c).verify()
        except ActionException:
            return False
        return True


class MarkAction(SeqAction[TTTGame, TTTPlayer]):
    def __init__(self, game: TTTGame, actor: TTTPlayer, r: int, c: int):
        super().__init__(game, actor)

        self.r, self.c = r, c

    @property
    def next_actor(self) -> Optional[TTTPlayer]:
        if self.game.empty_coords and self.game.winner is None:
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
