from abc import ABC, abstractmethod

from .exception import GamePlayerException, GameTerminalException
from .utils import Log


class Action(ABC):
    def __init__(self, player):
        self.__player = player

    @property
    def player(self):
        return self.__player

    @property
    def game(self):
        return self.player.game

    def _validate(self):
        if self.game.terminal:
            raise GameTerminalException('Actions are not applicable to terminal games')
        elif self.chance != self.player.nature:
            raise GamePlayerException('Nature acts chance actions')

    def act(self):
        self._validate()

        if self.public:
            self.game.logs.append(Log(self))

    @property
    @abstractmethod
    def chance(self):
        pass

    @property
    @abstractmethod
    def public(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class SeqAction(Action, ABC):
    def _validate(self):
        super()._validate()

        if self.player is not self.game.player:
            raise GamePlayerException(f'{self.player} cannot act in turn')
