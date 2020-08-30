from ..game.actions import CachedActions
from ..poker.action import Put, Continue, Surrender, Peel, Showdown, Distribute
from .action import PreFlop


class NLHEPlayerActions(CachedActions):
    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            for amount in self._sample_amounts:
                actions.append(Put(self.game, self.player, amount))

            actions.append(Continue(self.game, self.player))

            if max(self.game.players.bets) > self.player.bet:
                actions.append(Surrender(self.game, self.player))

        return actions

    @property
    def _sample_amounts(self):
        if self.game.min_raise < self.player.total:
            return [self.game.min_raise, self.player.total]
        elif max(self.game.players.bets) < self.player.total:
            return [self.player.total]
        else:
            return []


class NLHENatureActions(CachedActions):
    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            if self.game.street == 0:
                actions.append(PreFlop(self.game, self.player, 2))
            elif self.game.street == 1:
                actions.append(Peel(self.game, self.player, 3))
            elif self.game.street == 2 or self.game.street == 3:
                actions.append(Peel(self.game, self.player, 1))
            elif self.game.street == 4:
                actions.append(Showdown(self.game, self.player))
            else:
                actions.append(Distribute(self.game, self.player))

        return actions
