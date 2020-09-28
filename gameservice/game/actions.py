from abc import ABC, abstractmethod

from ..exceptions import GameTerminalException


class Action(ABC):
    def __init__(self, game, player):
        if game.terminal:
            raise GameTerminalException("Action is unavailable on terminal games")

        self.game = game
        self.player = player

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def act(self):
        pass
