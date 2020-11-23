from .tictactoeaction import TicTacToeMarkAction
from .tictactoeinfoset import TicTacToeInfoSet
from ..game import Player


class TicTacToePlayer(Player):
    @property
    def payoff(self):
        if self.game.winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self.game.winner is self else -1

    @property
    def actions(self):
        if self.game.player is self:
            return [TicTacToeMarkAction(self, r, c) for r, c in self.game.empty_coords]
        else:
            return []

    @property
    def info_set(self):
        return TicTacToeInfoSet(self)
