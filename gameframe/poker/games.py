from typing import Sequence

from gameframe.poker.bases import PokerGame
from gameframe.poker.stages import DealingStage, NLBettingStage
from gameframe.poker.utils import StandardDeck, StandardEvaluator


class NLTexasHEGame(PokerGame):
    """NLTexasHEGame is the class for no-limit texas hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], stacks: Sequence[int]):
        super().__init__([
            DealingStage(self, [False, False], 0), NLBettingStage(self),  # Pre-flop
            DealingStage(self, [], 3), NLBettingStage(self),  # Flop
            DealingStage(self, [], 1), NLBettingStage(self),  # Turn
            DealingStage(self, [], 1), NLBettingStage(self),  # River
        ], StandardDeck(), StandardEvaluator(), ante, blinds, stacks)
