from .action import NLHEPreFlop
from ..game.actions import CachedActions
from ..poker.action import Peel, Showdown, Distribute


class NLHENatureActions(CachedActions):
    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            if self.game.street == 0:
                actions.append(NLHEPreFlop(self.game, self.player))
            elif self.game.street == 1:
                actions.append(Peel(self.game, self.player, 3))
            elif self.game.street == 2 or self.game.street == 3:
                actions.append(Peel(self.game, self.player, 1))
            elif self.game.street == 4:
                actions.append(Showdown(self.game, self.player))
            else:
                actions.append(Distribute(self.game, self.player))

        return actions
