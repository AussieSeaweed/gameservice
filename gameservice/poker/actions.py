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
                bet_sizes = []

                if self.game.context.min_raise <= self.player.total:
                    bet_sizes.extend(self.game.bet_sizes(self.game.context.min_raise, self.player.total))
                elif max(self.game.players.bets) < self.player.total:
                    bet_sizes.append(self.player.total)

                for amount in bet_sizes:
                    actions.append(Put(self.game, self.player, amount))

        return actions
