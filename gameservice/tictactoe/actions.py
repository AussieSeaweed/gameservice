from ..game.actions import CachedActions
from .action import Mark


class TicTacToeActions(CachedActions):
    def _cache_actions(self):
        if self.game.terminal:
            return []
        else:
            return [Mark(self.game, self.player, r, c) for r, c in self.game.context.empty_coords]
