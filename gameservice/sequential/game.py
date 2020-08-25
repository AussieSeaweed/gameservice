from abc import ABC, abstractmethod

from ..game.game import Game


class SequentialGame(Game, ABC):
    @property
    @abstractmethod
    def player(self):
        pass


class TurnAlternationGame(SequentialGame, ABC):
    """
    No nature/chance events
    """

    initial_turn = 0

    def __init__(self):
        super().__init__()

        self.__turn = self.initial_turn

    @property
    def player(self):
        return None if self.terminal else self.players[self.__turn]

    def update(self):
        self.__turn = (self.__turn + 1) % len(self.players)
