from abc import ABC, abstractmethod

from ..exceptions import TerminalGameException


class Action(ABC):
    def __init__(self, game, player):
        if game.terminal:
            raise TerminalGameException

        self.game = game
        self.player = player

    @property
    @abstractmethod
    def label(self):
        pass

    def act(self):
        self.game.logs.append([self.player, self.label])
