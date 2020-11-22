from abc import ABC, abstractmethod

from .exception import GameInterruptionException, GamePlayerException, GameTerminalException


class Action(ABC):
    def __init__(self, player):
        if player.game.terminal:
            raise GameTerminalException('Actions are not applicable to terminal games')
        elif self.chance != player.nature:
            raise GamePlayerException('Nature acts chance actions')

        self.__player = player
        self.__num_logs = len(player.game.logs)

    @property
    def player(self):
        return self.__player

    @property
    def game(self):
        return self.player.game

    def act(self):
        if self.__num_logs != len(self.game.logs):
            raise GameInterruptionException('Game was modified since the creation of the action')

        self.game.log(self)

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


class SequentialAction(Action, ABC):
    def __init__(self, player):
        super().__init__(player)

        if player is not self.game.player:
            raise GamePlayerException(f'{player} cannot act in turn')
