"""
This module defines game utilities in gameservice.
"""


class Log:
    """
    This is a class that represents a log of an action taken in the game.
    """

    def __init__(self, action):
        """
        Constructs the Log instance that records the string representation of the action and the player who took the
        action.
        :param action: The action taken in the game
        """
        self.__action_str = str(action)
        self.__player_str = str(action.player)

    def __str__(self):
        """
        Returns the string representation of the log containing the information about the action taken and the player
        who took the action.
        :return: The string representation of the log
        """
        return f'{self.__player_str}: {self.__action_str}'
