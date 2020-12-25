"""
This module defines tic tac toe info-sets in gameservice.
"""
from ..game import SequentialInfoSet


class TicTacToeInfoSet(SequentialInfoSet):
    """
    This is a class that represents tic tac toe info-sets.
    """

    @property
    def environment_info(self):
        return {
            **super().environment_info,
            'board': self.game.environment.board,
            'empty_coords': self.game.environment.empty_coords,
            'winner': None if self.game.environment.winner is None else str(self.game.environment.winner),
        }
