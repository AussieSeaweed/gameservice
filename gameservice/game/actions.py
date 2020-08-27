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


class EmtpyActions(Actions):
    def __len__(self):
        return 0

    def __getitem__(self, item):
        raise IndexError

    def __iter__(self):
        return iter([])


class SingleActions(Actions):
    action_type = None

    def __init__(self, game, player):
        super().__init__(game, player)

        self.__action = self._create_action()

    def _create_action(self):
        return self.action_type(self.game, self.player)

    def __len__(self):
        return 1

    def __getitem__(self, item):
        if item == 0:
            return self.__action
        else:
            raise IndexError

    def __iter__(self):
        return iter([self.__action])
