"""
This module defines tic tac toe games in gameservice.
"""
from .environments import TTTEnvironment
from .players import TTTPlayer
from ..game import SeqGame


class TTTGame(SeqGame):
    """
    This is a class that represents tic tac toe games.
    """

    def _create_environment(self):
        """
        Creates a tic tac toe environment.

        :return: a tic tac toe environment
        """
        return TTTEnvironment(self)

    def _create_nature(self):
        """
        Returns None as tic tac toe games do not have nature.

        :return: None
        """
        return None

    def _create_players(self):
        """
        Creates tic tac toe players.

        :return: a list of tic tac toe players
        """
        return [TTTPlayer(self) for _ in range(2)]

    @property
    def _initial_player(self):
        """
        :return: the initial player of the tic tac toe game
        """
        return self.players[0]
