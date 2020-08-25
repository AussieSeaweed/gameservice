from abc import ABC, abstractmethod


class Actions(ABC):
    def __init__(self, game, player):
        self.__game = game
        self.__player = player

    @property
    def game(self):
        return self.__game

    @property
    def player(self):
        return self.__player

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __iter__(self):
        pass


class CachedActions(Actions, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        self.__actions = {action.label: action for action in self._cache_actions()}

    @abstractmethod
    def _cache_actions(self):
        pass

    def __len__(self):
        return len(self.__actions)

    def __getitem__(self, item):
        return self.__actions[item]

    def __iter__(self):
        return iter(self.__actions.keys())
