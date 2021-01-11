from gameframe.game import Actor
from gameframe.tictactoe.actions import MarkAction


class TicTacToeNature(Actor):
    """TicTacToeNature is the class for tic tac toe natures."""

    @property
    def actions(self):
        return []

    @property
    def payoff(self):
        return 0


class TicTacToePlayer(Actor):
    """TicTacToePlayer is the class for tic tac toe players."""

    @property
    def actions(self):
        if self is self.game.actor:
            return [MarkAction(self, r, c) for r, c in self.game.environment.empty_coordinates]
        else:
            return []

    @property
    def payoff(self):
        if self.game.environment.winner is None:
            return 0 if self.game.is_terminal else -1
        else:
            return 1 if self is self.game.environment.winner else -1

    def mark(self, r, c):
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        :raise: GameFrameException if the player cannot mark the cell
        """
        MarkAction(self, r, c).act()
