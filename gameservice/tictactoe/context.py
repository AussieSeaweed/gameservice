from ..game.context import Context


class TicTacToeContext(Context):
    def __init__(self, game):
        super().__init__(game)

        self.__board = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]

    @property
    def info(self):
        return {
            **super().info,
            "board": self.__board,
            "empty_coords": self.empty_coords,
            "winning_coords": self.winning_coords,
        }

    @property
    def board(self):
        return self.__board

    @property
    def empty_coords(self):
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def winning_coords(self):
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return [[0, i], [1, i], [2, i]]
            elif self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return [[i, 0], [i, 1], [i, 2]]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return [[0, 0], [1, 1], [2, 2]]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return [[0, 2], [1, 1], [2, 0]]

        return None
