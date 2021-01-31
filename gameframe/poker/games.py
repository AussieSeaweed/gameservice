from typing import Sequence

from gameframe.poker.bases import PokerGame
from gameframe.poker.rounds import DealingRound, NLBettingRound
from gameframe.poker.utils import StandardDeck, StandardEvaluator


class NLTexasHEGame(PokerGame):
    def __init__(self, ante: int, blinds: Sequence[int], stacks: Sequence[int]):
        super().__init__([
            DealingRound(self, [False, False], 0),
            NLBettingRound(self),
            DealingRound(self, [], 3),
            NLBettingRound(self),
            DealingRound(self, [], 1),
            NLBettingRound(self),
            DealingRound(self, [], 1),
            NLBettingRound(self),
        ], StandardDeck(), StandardEvaluator(), ante, blinds, stacks)
