from .actions import NLHEPreFlop
from ..game.actionset import CachedActionSet
from ..poker.actions import Peel, Showdown, Distribute


class NLHENatureActionSet(CachedActionSet):
    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            if self.game.context.street == 0:
                actions.append(NLHEPreFlop(self.game, self.player))
            elif self.game.context.street == 1:
                actions.append(Peel(self.game, self.player, 3))
            elif self.game.context.street == 2 or self.game.context.street == 3:
                actions.append(Peel(self.game, self.player, 1))
            elif self.game.context.street == 4:
                actions.append(Showdown(self.game, self.player))
            else:
                actions.append(Distribute(self.game, self.player))

        return actions
