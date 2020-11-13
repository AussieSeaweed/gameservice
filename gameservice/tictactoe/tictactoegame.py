from .tictactoeplayer import TicTacToePlayer
from ..game import SequentialGame


class TicTacToeGame(SequentialGame):
    def __init__(self):
        super().__init__()

        self.__board = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]

    def _create_players(self):
        return [TicTacToePlayer(self) for _ in range(2)]

    def _create_nature(self):
        return None

    @property
    def _initial_player(self):
        return self.players[0]

    @property
    def board(self):
        return self.__board

    @property
    def empty_coords(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return self.players[self.board[i][0]]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return self.players[self.board[0][i]]

        if self.board[1][1] is not None and (self.board[0][0] == self.board[1][1] == self.board[2][2] or
                                             self.board[0][2] == self.board[1][1] == self.board[2][0]):
            return self.players[self.board[1][1]]

        return None
