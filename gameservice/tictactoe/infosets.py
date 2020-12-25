"""
This module defines tic tac toe info-sets in gameservice.
"""
from ..game import SequentialInfoSet


class TicTacToeInfoSet(SequentialInfoSet):
    """
    This is a class that represents tic tac toe info-sets.
    """

    def environment_info(self, environment):
        return {
            **super().environment_info(environment),
            'board': environment.board,
            'empty_coords': environment.empty_coords,
            'winner': None if environment.winner is None else self.player_info(environment.winner),
        }
