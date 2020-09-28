from abc import ABC, abstractmethod

from ..game.game import Game


class SequentialGame(Game, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player = self._get_initial_player()

    @abstractmethod
    def _get_initial_player(self):
        pass

    @property
    def terminal(self):
        return self.player is None
