from .environments import TicTacToeEnvironment
from .players import TicTacToeNature, TicTacToePlayer
from ..sequential import SequentialGame


class TicTacToeGame(SequentialGame):
    """TicTacToeGame is the class for tic tac toe games."""

    def _create_environment(self):
        return TicTacToeEnvironment(self)

    def _create_nature(self):
        return TicTacToeNature(self)

    def _create_players(self):
        return [TicTacToePlayer(self), TicTacToePlayer(self)]

    @property
    def _initial_player(self):
        return self.players[0]
