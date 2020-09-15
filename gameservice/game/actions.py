from abc import ABC, abstractmethod


class Actions(ABC):
    def __init__(self, game, player):
        self.game = game
        self.player = player

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

        self.__actions = {action.name: action for action in self._create_actions()}

    @abstractmethod
    def _create_actions(self):
        pass

    def __len__(self):
        return len(self.__actions)

    def __getitem__(self, item):
        return self.__actions[item]

    def __iter__(self):
        return iter(self.__actions)


class EmptyActions(Actions):
    def __len__(self):
        return 0

    def __getitem__(self, item):
        raise KeyError

    def __iter__(self):
        return iter(())
