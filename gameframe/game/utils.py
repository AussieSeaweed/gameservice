"""
This module defines utilities in gameframe.
"""
from typing import TypeVar

G = TypeVar('G')
E = TypeVar('E')
N = TypeVar('N')
P = TypeVar('P')


class Log:
    """
    This is a class that represents logs. Each log records information about an action taken in the game.
    """

    def __init__(self, action):
        self.__action_str = str(action)
        self.__player_str = str(action.player)

    def __str__(self):
        return f'{self.__player_str}: {self.__action_str}'
