from __future__ import annotations

from typing import Iterator, MutableSequence, Optional, Sequence, TypeVar

from gameframe.game import Actor
from gameframe.sequential import SeqAction, SeqEnv, SeqGame


class TTTGame(SeqGame['TTTEnv', 'TTTNature', 'TTTPlayer']):
    """TTTGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        players = (TTTPlayer(self), TTTPlayer(self))

        super().__init__(TTTEnv(self, players[0]), TTTNature(self), players)


class TTTEnv(SeqEnv[TTTGame, 'TTTNature', 'TTTPlayer']):
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


class TTTNature(Actor[TTTGame]):
    """TTTNature is the class for tic tac toe natures."""

    @property
    def actions(self) -> Sequence[TTTAction[TTTNature]]:
        return []


class TTTPlayer(Actor[TTTGame], Iterator['TTTPlayer']):
    """TTTPlayer is the class for tic tac toe players."""

    def __next__(self) -> TTTPlayer:
        return self.game.players[(self.game.players.index(self) + 1) % len(self.game.players)]

    @property
    def actions(self) -> Sequence[TTTAction[TTTPlayer]]:
        from gameframe.tictactoe.actions import MarkAction

        if self is self.game.env.actor:
            return [MarkAction(self.game, self, r, c) for r, c in self.game.env.empty_coords]
        else:
            return []

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        """
        from gameframe.tictactoe.actions import MarkAction

        MarkAction(self.game, self, r, c).act()


A = TypeVar('A', TTTNature, TTTPlayer)


class TTTAction(SeqAction[TTTGame, A]):
    """TicTacToeAction is the class for tic tac toe actions."""
    pass
