from abc import ABC, abstractmethod


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

    def log(self, action_name):
        self.__logs.append(Log(action_name))

    @property
    @abstractmethod
    def terminal(self):
        pass


class SequentialGame(Game, ABC):
    def __init__(self):
        super().__init__()

        self.player = self._get_initial_player()

    @abstractmethod
    def _get_initial_player(self):
        pass

    @property
    def terminal(self):
        return self.player is None


class Log:
    def __init__(self, action_name):
        self.__action_name = action_name

    @property
    def action_name(self):
        return self.__action_name
