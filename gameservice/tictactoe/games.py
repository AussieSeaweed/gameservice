"""
This module defines tic tac toe games in gameservice.
"""
from .environments import TicTacToeEnvironment
from .players import TicTacToePlayer
from ..game import SequentialGame


class TicTacToeGame(SequentialGame):
    """
    This is a class that represents tic tac toe games.
    """

    def create_environment(self):
        return TicTacToeEnvironment(self)

    def create_nature(self):
        return None

    def create_player(self):
        return [TicTacToePlayer(self) for _ in range(2)]

    @property
    def initial_player(self):
        return self.players[0]
