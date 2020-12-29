from .actions import MarkAction
from ..game import Player


class TicTacToePlayer(Player):
    """TicTacToePlayer is the class for tic tac toe players."""

    @property
    def actions(self):
        if self is self.game.player:
            return [MarkAction(self, r, c) for r, c in self.game.environment._empty_coordinates]
        else:
            return []

    @property
    def payoff(self):
        if self.game.environment._winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self.game.environment._winner is self else -1


class TicTacToeNature(Player):
    """TicTacToeNature is the class for tic tac toe natures."""

    @property
    def actions(self):
        return []

    @property
    def payoff(self):
        return 0
