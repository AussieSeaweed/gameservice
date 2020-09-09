from ..game.actions import CachedActions
from .action import Put, Continue, Surrender


class NLPlayerActions(CachedActions):
    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            if max(self.game.players.bets) > self.player.bet:
                actions.append(Surrender(self.game, self.player))

            actions.append(Continue(self.game, self.player))

            if self.game.players.num_relevant > 1:
                if self.game.min_raise < self.player.total:
                    for amount in self.game.bet_sizes(self.game.min_raise, self.player.total):
                        actions.append(Put(self.game, self.player, amount))
                elif max(self.game.players.bets) < self.player.total:
                    actions.append(Put(self.game, self.player, self.player.total))

        return actions
