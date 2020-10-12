from ..sequential.players import SequentialPlayer


class TicTacToePlayer(SequentialPlayer):
    @property
    def payoff(self):
        if not self.game.context.empty_coords:
            return 0
        elif self.game.context.winning_coords:
            r, c = self.game.context.winning_coords[0]

            return 1 if self.game.context.board[r][c] == self.index else -1
        else:
            return -1
