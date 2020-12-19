"""
This module defines tic tac toe info-sets in gameservice.
"""
from ..game import SeqInfoSet


class TTTInfoSet(SeqInfoSet):
    """
    This is a class that represents tic tac toe info-sets.
    """

    @classmethod
    def environment_info(cls, environment):
        """
        Serializes the tic tac toe environment.

        :param environment: the tic tac toe environment of the tic tac toe info-set
        :return: the dictionary representation of the tic tac toe environment information
        """
        return {
            **super().environment_info(environment),
            'board': environment.board,
        }
