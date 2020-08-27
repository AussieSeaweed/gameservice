from .action import Mark
from ..game.actions import CachedActions


class TicTacToeActions(CachedActions):
    def _cache_actions(self):
        if self.game.player is not self.player:
            return []
        else:
            return [Mark(self.game, self.player, r, c) for r, c in self.game.context.empty_coords]
