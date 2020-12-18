"""
This module defines tic tac toe environments in gameservice.
"""
from ..game import Environment


class TTTEnvironment(Environment):
    """
    This is a class that represents tic tac toe environments.
    """

    def __init__(self, game):
        """
        Constructs the TicTacToeEnvironment instance. Initializes the board.
        :param game: the game in which the tic tac toe environment belongs
        """
        super().__init__(game)

        self.__board = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]

    @property
    def board(self):
        """
        :return: the board of the tic tac toe environment
        """
        return self.__board

    @property
    def empty_coords(self):
        """
        :return: a list of empty coordinates of the board of the tic tac toe environment
        """
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def winner(self):
        """
        Determines the winner of the tic tac toe game.
        :return: the winning player if it exists else None
        """
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return self.game.players[self.board[i][0]]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return self.game.players[self.board[0][i]]

        if self.board[1][1] is not None and (self.board[0][0] == self.board[1][1] == self.board[2][2] or
                                             self.board[0][2] == self.board[1][1] == self.board[2][0]):
            return self.game.players[self.board[1][1]]

        return None
