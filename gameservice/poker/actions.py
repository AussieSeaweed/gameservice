from abc import ABC, abstractmethod

from ..game.actions import CachedActions, SingleActions
from .action import Deal, Peel, Showdown, Distribute


class BettingActions(CachedActions, ABC):
    def _cache_actions(self):
        pass

    @abstractmethod
    def _sample_bets(self):
        pass


class DealingActions(SingleActions):
    action_type = Deal

    """Static member variables"""

    num_cards = None

    def _create_action(self):
        return Deal(self.game, self.player, self.num_cards)


class PeelingActions(SingleActions):
    action_type = Peel

    """Static member variables"""

    num_cards = None

    def _create_action(self):
        return Peel(self.game, self.player, self.num_cards)


class ShowdownActions(SingleActions):
    action_type = Showdown


class DistributingActions(SingleActions):
    action_type = Distribute
