from abc import ABC, abstractmethod
from typing import TypeVar

from gameframe.poker.bases import PokerNature, PokerPlayer
from gameframe.sequential import _SequentialAction

_A = TypeVar('_A', PokerPlayer, PokerNature)


class PokerAction(_SequentialAction[_A], ABC):
    def act(self) -> None:
        super().act()

        self.actor.game._update()


class DealingAction(PokerAction[PokerNature], ABC):
    @property
    @abstractmethod
    def deal_count(self) -> int:
        ...


class HoleDealingAction(DealingAction):
    ...


class BoardDealingAction(DealingAction):
    ...


class BettingStageAction(PokerAction[PokerPlayer], ABC):
    ...


class FoldAction(BettingStageAction):
    ...


class CheckCallAction(BettingStageAction):
    ...


class BetRaiseAction(BettingStageAction):
    ...


class DiscardDrawAction(PokerAction[PokerPlayer]):
    ...


class ShowdownAction(PokerAction[PokerPlayer]):
    ...
