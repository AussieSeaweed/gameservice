"""
This module defines tic tac toe actions in gameframe.
"""
from abc import ABC

from ..game import ActionArgumentException, SequentialAction


class TicTacToeAction(SequentialAction, ABC):
    """
    This is a class that represents tic tac toe actions.
    """

    @property
    def chance(self):
        return False

    @property
    def public(self):
        return True


class MarkAction(TicTacToeAction):
    """
    This is a class that represents mark actions.
    """

    def __init__(self, player, r, c):
        super().__init__(player)

        self.__r = r
        self.__c = c

    def validate(self):
        super().validate()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise ActionArgumentException('The cell coordinates are invalid')
        elif self.game.environment.board[self.__r][self.__c] is not None:
            raise ActionArgumentException('The cell is already occupied')

    def act(self):
        super().act()

        self.game.environment.board[self.__r][self.__c] = self.player.index

        if self.game.environment.empty_coords and self.game.environment.winner is None:
            self.game.player = next(self.player)
        else:
            self.game.player = None

    def __str__(self):
        return f'Mark row {self.__r} column {self.__c}'
