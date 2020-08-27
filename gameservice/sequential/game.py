from abc import ABC

from ..game.game import Game


class SequentialGame(Game, ABC):
    player = None

    @property
    def terminal(self):
        return self.player is None
