from abc import ABC
from collections import Sequence

from gameframe.poker.bases import PokerGame
from gameframe.poker.stages import DealingStage, NLBettingStage, ShowdownStage
from gameframe.poker.utils import Deck, Evaluator, GreekEvaluator, OmahaEvaluator, StandardDeck, StandardEvaluator


class NLHEGame(PokerGame, ABC):
    """NLHEGame is the class for no-limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__([
            DealingStage(self, [False for _ in range(hole_card_count)], 0), NLBettingStage(self, max_delta),  # Pre-flop
            DealingStage(self, [], 3), NLBettingStage(self, max_delta),  # Flop
            DealingStage(self, [], 1), NLBettingStage(self, max_delta),  # Turn
            DealingStage(self, [], 1), NLBettingStage(self, max_delta),  # River
            ShowdownStage(self),  # Showdown
        ], deck, evaluator, ante, blinds, starting_stacks)


class NLTHEGame(NLHEGame):
    """NLTHEGame is the class for no-limit texas Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


class NLOHEGame(NLHEGame):
    """NLOHEGame is the class for no-limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


class NLGHEGame(NLHEGame):
    """NLGHEGame is the class for no-limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)
