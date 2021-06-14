"""This module defines various components of tic tac toe games."""
from random import choice

from gameframe import Actor, GameFrameError, SequentialGame, _SequentialAction


class TicTacToeGame(SequentialGame):
    """TicTacToeGame is the class for tic tac toe games."""

    def __init__(self):
        super().__init__(0, Actor(self), (TicTacToePlayer(self), TicTacToePlayer(self)))

        self._board = [[None, None, None], [None, None, None], [None, None, None]]

    @property
    def board(self):
        """Returns the board of this tic tac toe game.

        :return: The board of this tic tac toe game.
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_coordinates(self):
        """Returns the empty coordinates of the board of this tic tac toe game.

        :return: The list of the empty coordinates of the board.
        """
        return tuple((r, c) for r in range(3) for c in range(3) if self._board[r][c] is None)

    @property
    def winner(self):
        """Returns the winner of this tic tac toe game.

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

    def mark(self, *coordinates):
        """Parses the coordinates (tuples of two integers) as mark actions and applies them to this tic tac toe game.

        :param coordinates: The coordinates to mark.
        :return: This game.
        """
        for r, c in coordinates:
            self.actor.mark(r, c)

        return self


class TicTacToePlayer(Actor):
    """TicTacToePlayer is the class for tic tac toe players."""

    def __repr__(self):
        return 'O' if self.game.players[0] is self else 'X'

    def mark(self, r=None, c=None):
        """Marks the cell of the board at the optionally specified coordinates.

        If the row and column numbers are not supplied, they are randomly determined among empty cells.
        Either none or all of r and c must be provided.

        :param r: The optional row number of the cell.
        :param c: The optional column number of the cell.
        :return: None.
        """
        _MarkAction(r, c, self).act()

    def can_mark(self, r=None, c=None):
        """Determines if the cell of the board at the coordinates can be marked.

        Either none or all of r and c must be provided.

        :param r: The optional row number of the cell.
        :param c: The optional column number of the cell.
        :return: True if the cell can be marked, else False.
        """
        return _MarkAction(r, c, self).can_act()


class _MarkAction(_SequentialAction):
    def __init__(self, r, c, actor):
        super().__init__(actor)

        if (r is None) ^ (c is None):
            raise ValueError('Either all or no row-column coordinates should be supplied')

        self.r = r
        self.c = c

    def act(self):
        super().act()

        if self.r is None or self.c is None:
            self.r, self.c = choice(self.game.empty_coordinates)

        self.game._board[self.r][self.c] = self.actor

        if self.game.empty_coordinates and self.game.winner is None:
            self.game._actor = self.game.players[self.game.players[0] is self.actor]
        else:
            self.game._actor = None

    def verify(self):
        super().verify()

        if self.r is not None and self.c is not None:
            if not isinstance(self.r, int) or not isinstance(self.c, int):
                raise GameFrameError('The coordinates must be of type integer')
            elif not (0 <= self.r < 3 and 0 <= self.c < 3):
                raise GameFrameError('The coordinates must be within bounds (from 0 to 3 inclusive)')
            elif self.game._board[self.r][self.c] is not None:
                raise GameFrameError('The cell to be marked must be empty')
