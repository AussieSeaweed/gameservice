"""
This module defines tic tac toe actions in gameservice.
"""
from abc import ABC

from ..game import ActionArgumentException, SequentialAction


class TicTacToeAction(SequentialAction, ABC):
    """
    This is a class that represents tic tac toe actions.
    """
    pass


class MarkAction(TicTacToeAction):
    """
    This is a class that represents mark actions.
    """

    def __init__(self, player, r, c):
        """
        Constructs a MarkAction instance. Stores the coordinates of the cell.

        :param player: the acting player
        :param r: the row number of the cell
        :param c: the column number of the cell
        """
        super().__init__(player)

        self.__r = r
        self.__c = c

    def validate(self):
        """
        Validates the integrity of the tic tac toe mark action.

        :return: None
        :raise GameActionArgumentException: if the cell coordinate is invalid
        :raise TicTacToeCellException: if the cell is occupied
        """
        super().validate()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise ActionArgumentException('The cell coordinates are invalid')
        elif self.game.environment.board[self.__r][self.__c] is not None:
            raise ActionArgumentException('The cell is already occupied')

    def act(self):
        """
        Applies the tic tac toe mark action to the associated tic tac toe game.

        :return: None
        :raise GameServiceException: if tic tac toe game validation fails
        """
        super().act()

        self.game.environment.board[self.__r][self.__c] = self.player.index

        if self.game.environment.empty_coords and self.game.environment.winner is None:
            self.game.player = next(self.player)
        else:
            self.game.player = None

    @property
    def chance(self):
        """
        :return: False as tic tac toe mark actions are not chance actions
        """
        return False

    @property
    def public(self):
        """
        :return: True as tic tac toe mark actions are public
        """
        return True

    def __str__(self):
        """
        Converts the tic tac toe mark action into a string representation.

        :return: a string representation of the mark action
        """
        return f'Mark row {self.__r} column {self.__c}'
