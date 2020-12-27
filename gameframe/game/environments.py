from abc import ABC
from typing import Generic
from .utils import G, E, N, P


class Environment(Generic[G, E, N, P], ABC):
    """Environment is the base class for all environments."""

    def __init__(self, game: G):
        self.__game: G = game

    @property
    def game(self) -> G:
        """
        :return: the game of the environment
        """
        return self.__game
