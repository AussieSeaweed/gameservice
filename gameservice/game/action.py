from abc import ABC, abstractmethod

from .exception import GameTerminalException, GameInterruptionException, GamePlayerException


class Action(ABC):
    def __init__(self, player):
        if player.game.terminal:
            raise GameTerminalException("Actions are not applicable to terminal games")

        if self.chance != player.nature:
            raise GamePlayerException("Nature acts chance actions")

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
            raise GameInterruptionException("Game was modified since the action's creation")

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

        if player != self.game.player:
            raise GamePlayerException("Player cannot act in the sequential game")
