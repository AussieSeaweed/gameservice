from abc import ABC, abstractmethod

from gameservice.game.actionsets import CachedActionSet
from ..actions import Put, Continue, Surrender


class PokerPlayerActionSet(CachedActionSet, ABC):
    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            if max(self.game.players.bets) > self.player.bet:
                actions.append(Surrender(self.game, self.player))

            actions.append(Continue(self.game, self.player))

            if self.game.players.num_relevant > 1:
                for amount in self.bet_sizes:
                    actions.append(Put(self.game, self.player, amount))

        return actions

    @property
    @abstractmethod
    def bet_sizes(self):
        pass


class NLPokerPlayerActionsSet(PokerPlayerActionSet):
    @property
    def bet_sizes(self):
        bet_sizes = []

        if self.game.context.min_raise <= self.player.total:
            bet_sizes.extend(range(self.game.context.min_raise, self.player.total + 1))
        elif max(self.game.players.bets) < self.player.total:
            bet_sizes.append(self.player.total)

        return bet_sizes
