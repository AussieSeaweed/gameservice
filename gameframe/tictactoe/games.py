from .environments import TicTacToeEnvironment
from .players import TicTacToePlayer, TicTacToeNature
from ..sequential import SequentialGame


class TicTacToeGame(SequentialGame['TicTacToeGame', TicTacToeEnvironment, None, TicTacToePlayer]):
    """
    This is a class that represents tic tac toe games.
    """

    def create_environment(self):
        return TicTacToeEnvironment(self)

    def create_nature(self):
        return TicTacToeNature(self)

    def create_players(self):
        return [TicTacToePlayer(self) for _ in range(2)]

    @property
    def initial_player(self):
        return self.players[0]
