from abc import ABC, abstractmethod
from ..exceptions import TerminalGameException


class Action(ABC):
    def __init__(self, game, player):
        if game.terminal:
            raise TerminalGameException

        self.__game = game
        self.__player = player

    @property
    def game(self):
        return self.__game

    @property
    def player(self):
        return self.__player

    @property
    @abstractmethod
    def label(self):
        pass

    @abstractmethod
    def act(self):
        pass
