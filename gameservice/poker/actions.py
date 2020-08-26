from abc import ABC, abstractmethod

from ..game.actions import CachedActions


class BettingActions(CachedActions, ABC):
    def _cache_actions(self):
        pass

    @abstractmethod
    def _sample_bets(self):
        pass


class DealActions(CachedActions):
    def _cache_actions(self):
        pass


class PeelActions(CachedActions):
    def _cache_actions(self):
        pass


class ResultActions(CachedActions):
    def _cache_actions(self):
        pass
