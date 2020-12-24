"""
This module defines tic tac toe info-sets in gameservice.
"""
from ..game import SequentialInfoSet


class TicTacToeInfoSet(SequentialInfoSet):
    """
    This is a class that represents tic tac toe info-sets.
    """

    @classmethod
    def environment_info(cls, environment):
        return {
            **super().environment_info(environment),
            'board': environment.board,
        }
