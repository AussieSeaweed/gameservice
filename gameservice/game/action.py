from abc import ABC, abstractmethod

from ..exceptions import GameTerminalException, GameInterruptedException, GamePlayerException


class Action(ABC):
    def __init__(self, player):
        if player.game.terminal:
            raise GameTerminalException("Actions are not applicable to terminal games")

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
            raise GameInterruptedException("Game was modified since the action's creation")

        self.game.log(self.name)

    @property
    @abstractmethod
    def name(self):
        pass


class SequentialAction(Action, ABC):
    def __init__(self, player):
        super().__init__(player)

        if player != self.game.player:
            raise GamePlayerException("Player cannot act in the sequential game")
