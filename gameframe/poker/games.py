from typing import Sequence

from gameframe.poker.bases import PokerGame
from gameframe.poker.stages import DealingStage, NLBettingStage, ShowdownStage
from gameframe.poker.utils import StandardDeck, StandardEvaluator


class NLTHEGame(PokerGame):
    """NLTHEGame is the class for no-limit texas hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__([
            DealingStage(self, [False, False], 0), NLBettingStage(self, max_delta),  # Pre-flop
            DealingStage(self, [], 3), NLBettingStage(self, max_delta),  # Flop
            DealingStage(self, [], 1), NLBettingStage(self, max_delta),  # Turn
            DealingStage(self, [], 1), NLBettingStage(self, max_delta),  # River
            ShowdownStage(self),  # Showdown
        ], StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)
