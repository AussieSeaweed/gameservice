from ..game import Environment


class TicTacToeEnvironment(Environment):
    """TicTacToeGame is the class for tic tac toe environments."""

    def __init__(self, game):
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
    def _empty_coordinates(self):
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def _winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return self.board[i][0]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None or \
                self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return self.board[1][1]

        return None

    @property
    def _information(self):
        return {
            'board': self.board,
        }
