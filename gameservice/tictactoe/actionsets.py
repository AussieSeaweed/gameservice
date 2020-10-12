from .actions import Mark
from ..game.actionsets import CachedActionSet


class TicTacToeActionSet(CachedActionSet):
    def _create_actions(self):
        if self.game.player is not self.player:
            return []
        else:
            return [Mark(self.game, self.player, r, c) for r, c in self.game.context.empty_coords]
