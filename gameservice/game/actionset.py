from abc import ABC, abstractmethod

from ..exceptions import ActionNotFoundException


class ActionSet(ABC):
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


class CachedActionSet(ActionSet, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        self.__actions = {action.name: action for action in self._create_actions()}

    @abstractmethod
    def _create_actions(self):
        pass

    def __len__(self):
        return len(self.__actions)

    def __getitem__(self, item):
        try:
            return self.__actions[item]
        except KeyError:
            raise ActionNotFoundException(f"Action {item} is not found")

    def __iter__(self):
        return iter(self.__actions)


class EmptyActionSet(ActionSet):
    def __len__(self):
        return 0

    def __getitem__(self, item):
        raise ActionNotFoundException(f"Action {item} is not found")

    def __iter__(self):
        return iter(())
