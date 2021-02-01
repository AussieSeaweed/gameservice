from __future__ import annotations

from typing import Iterator, MutableSequence, Optional, Sequence

from gameframe.game import ActionException
from gameframe.game.generics import Actor
from gameframe.sequential.generics import SeqAction, SeqEnv, SeqGame


class TTTGame(SeqGame['TTTEnv', Actor['TTTGame'], 'TTTPlayer']):
    """TTTGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        players = (TTTPlayer(self), TTTPlayer(self))

        super().__init__(TTTEnv(self, players[0]), Actor(self), players)


class TTTEnv(SeqEnv[TTTGame, Actor['TTTGame'], 'TTTPlayer']):
    """TTTEnv is the class for tic tac toe environments."""

    def __init__(self, game: TTTGame, actor: TTTPlayer):
        super().__init__(game, actor)

        self._board: MutableSequence[MutableSequence[Optional[TTTPlayer]]] = [[None, None, None],
                                                                              [None, None, None],
                                                                              [None, None, None]]

    @property
    def board(self) -> Sequence[Sequence[Optional[TTTPlayer]]]:
        """
        :return: the board of this tic tac toe environment
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_coords(self) -> Sequence[Sequence[int]]:
        """
        :return: the list of empty coordinates of the board
        """
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def winner(self) -> Optional[TTTPlayer]:
        """
        :return: the winning player of the tic tac toe game if there is one, else None
        """
        for i in range(3):
            if self.board[i][0] is self.board[i][1] is self.board[i][2] is not None:
                return self.board[i][0]
            elif self.board[0][i] is self.board[1][i] is self.board[2][i] is not None:
                return self.board[0][i]

        if self.board[0][0] is self.board[1][1] is self.board[2][2] is not None \
                or self.board[0][2] is self.board[1][1] is self.board[2][0] is not None:
            return self.board[1][1]

        return None


class TTTPlayer(Actor[TTTGame], Iterator['TTTPlayer']):
    """TTTPlayer is the class for tic tac toe players."""

    def __next__(self) -> TTTPlayer:
        return self.game.players[(self.game.players.index(self) + 1) % len(self.game.players)]

    def __repr__(self) -> str:
        return 'O' if self.game.players[0] is self else 'X'

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        """
        MarkAction(self.game, self, r, c).act()


class MarkAction(SeqAction[TTTGame, TTTPlayer]):
    def __init__(self, game: TTTGame, actor: TTTPlayer, r: int, c: int):
        super().__init__(game, actor)

        self.r = r
        self.c = c

    def act(self) -> None:
        super().act()

        self.game.env._board[self.r][self.c] = self.actor

        if self.game.env.empty_coords and self.game.env.winner is None:
            self.game.env._actor = next(self.actor)
        else:
            self.game.env._actor = None

    def verify(self) -> None:
        super().verify()

        if not (0 <= self.r < 3 and 0 <= self.c < 3):
            raise ActionException('The coords are out of bounds')
        elif self.game.env.board[self.r][self.c] is not None:
            raise ActionException('The cell is not empty')
