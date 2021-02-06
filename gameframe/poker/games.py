from abc import ABC
from typing import Sequence

from gameframe.poker.bases import PokerGame
from gameframe.poker.stages import DealingStage, NLBettingStage, ShowdownStage
from gameframe.poker.utils import Deck, Evaluator, GreekEvaluator, OmahaEvaluator, StandardDeck, StandardEvaluator


class NLHEGame(PokerGame, ABC):
    """NLHEGame is the class for no-limit hold'em games."""

    def __init__(self, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__([
            DealingStage(self, [False, False], 0), NLBettingStage(self, max_delta),  # Pre-flop
            DealingStage(self, [], 3), NLBettingStage(self, max_delta),  # Flop
            DealingStage(self, [], 1), NLBettingStage(self, max_delta),  # Turn
            DealingStage(self, [], 1), NLBettingStage(self, max_delta),  # River
            ShowdownStage(self),  # Showdown
        ], deck, evaluator, ante, blinds, starting_stacks)


class NLTHEGame(NLHEGame):
    """NLTHEGame is the class for no-limit texas hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


class NLOHEGame(NLHEGame):
    """NLOHEGame is the class for no-limit omaha hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


class NLGHEGame(NLHEGame):
    """NLGHEGame is the class for no-limit greek hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)
