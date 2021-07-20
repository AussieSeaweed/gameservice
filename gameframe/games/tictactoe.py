"""This module defines various components of tic tac toe games."""
from itertools import filterfalse, product
from random import choice

from auxiliary import next_or_none

from gameframe.exceptions import GameFrameError
from gameframe.sequential import SequentialActor, SequentialGame, _SequentialAction


class TicTacToeGame(SequentialGame):
    """TicTacToeGame is the class for tic tac toe games."""

    def __init__(self):
        super().__init__(0, SequentialActor(self), (TicTacToePlayer(self), TicTacToePlayer(self)))

        self._board = [[None, None, None], [None, None, None], [None, None, None]]

    @property
    def board(self):
        """Returns the board of this tic tac toe game.

        :return: The board of this tic tac toe game.
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_cell_locations(self):
        """Returns the empty cell locations of the board of this tic tac toe game.

        :return: An iterator of the empty coordinates of the board.
        """
        return filterfalse(self._get_cell, product(range(3), range(3)))

    @property
    def winner(self):
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

    @property
    def loser(self):
        """Returns the loser of this tic tac toe game.

        :return: The losing player of the tic tac toe game if there is one, else None.
        """
        return None if self.winner is None else next(self.winner)

    def mark(self, *coordinates):
        """Parses the coordinates (tuples of two integers) as mark actions and applies them to this tic tac toe game.

        :param coordinates: The coordinates to mark.
        :return: This game.
        """
        for r, c in coordinates:
            self.actor.mark(r, c)

        return self

    def _get_cell(self, coords):
        return self.board[coords[0]][coords[1]]


class TicTacToePlayer(SequentialActor):
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

        self.r = r
        self.c = c

    def verify(self):
        super().verify()

        if self.r is not None and self.c is not None:
            if not isinstance(self.r, int) or not isinstance(self.c, int):
                raise TypeError('The coordinates must be of type integer')
            elif not (0 <= self.r < 3 and 0 <= self.c < 3):
                raise GameFrameError('The coordinates must be within bounds (from 0 to 3 inclusive)')
            elif self.actor.game.board[self.r][self.c] is not None:
                raise GameFrameError('The cell to be marked must be empty')
        elif self.r is not None or self.c is not None:
            raise ValueError('Either all or no row-column coordinates should be supplied')

    def apply(self):
        game = self.actor.game

        if self.r is None or self.c is None:
            self.r, self.c = choice(tuple(game.empty_cell_locations))

        game._board[self.r][self.c] = self.actor

        if next_or_none(game.empty_cell_locations) is not None and game.winner is None:
            game._actor = next(self.actor)
        else:
            game._actor = None
