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
        """
        Creates a tic tac toe environment.

        :return: a tic tac toe environment
        """
        return TicTacToeEnvironment(self)

    def create_nature(self):
        """
        Returns None as tic tac toe games do not have nature.

        :return: None
        """
        return None

    def create_player(self):
        """
        Creates tic tac toe players.

        :return: a list of tic tac toe players
        """
        return [TicTacToePlayer(self) for _ in range(2)]

    @property
    def initial_player(self):
        """
        :return: the initial player of the tic tac toe game
        """
        return self.players[0]
