from abc import ABC, abstractmethod

from .utils import Log


class Game(ABC):
    def __init__(self):
        self.__players = self._create_players()
        self.__nature = self._create_nature()
        self.__logs = []

    @abstractmethod
    def _create_players(self):
        pass

    @abstractmethod
    def _create_nature(self):
        pass

    @property
    def players(self):
        return self.__players

    @property
    def nature(self):
        return self.__nature

    @property
    def logs(self):
        return self.__logs

    def log(self, action):
        self.__logs.append(Log(action))

    @property
    @abstractmethod
    def terminal(self):
        pass


class SequentialGame(Game, ABC):
    def __init__(self):
        super().__init__()

        self.player = self._initial_player

    @property
    @abstractmethod
    def _initial_player(self):
        pass

    @property
    def terminal(self):
        return self.player is None
