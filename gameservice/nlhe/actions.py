from ..game.actions import CachedActions
from .action import Deal, Peel, Showdown, Distribute


class NLHEPlayerActions(CachedActions):
    def _create_actions(self):
        pass

    def _sample_bets(self):
        pass


class NLHENatureActions(CachedActions):
    def _create_actions(self):
        if self.game.phase == 0:
            return [Deal(self.game, self.player, 2)]
        elif self.game.phase == 1:
            return [Peel(self.game, self.player, 3)]
        elif self.game.phase == 2 or self.game.phase == 3:
            return [Peel(self.game, self.player, 1)]
        elif self.game.phase == 4:
            return [Showdown(self.game, self.player)]
        elif self.game.phase == 5:
            return [Distribute(self.game, self.player)]
