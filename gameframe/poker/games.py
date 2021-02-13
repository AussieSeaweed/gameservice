from abc import ABC
from collections import Sequence
from typing import final

from pokertools import Deck, Evaluator, GreekEvaluator, OmahaEvaluator, StandardDeck, StandardEvaluator

from gameframe.poker.bases import PokerGame
from gameframe.poker.stages import BoardCardDealingStage, HoleCardDealingStage, NLBettingStage, ShowdownStage


class NLHEGame(PokerGame, ABC):
    """NLHEGame is the class for no-limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__([
            HoleCardDealingStage(self, hole_card_count, False), NLBettingStage(self, max_delta),  # Pre-flop
            BoardCardDealingStage(self, 3), NLBettingStage(self, max_delta),  # Flop
            BoardCardDealingStage(self, 1), NLBettingStage(self, max_delta),  # Turn
            BoardCardDealingStage(self, 1), NLBettingStage(self, max_delta),  # River
            ShowdownStage(self),  # Showdown
        ], deck, evaluator, ante, blinds, starting_stacks)


@final
class NLTHEGame(NLHEGame):
    """NLTHEGame is the class for no-limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class NLOHEGame(NLHEGame):
    """NLOHEGame is the class for no-limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class NLGHEGame(NLHEGame):
    """NLGHEGame is the class for no-limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)
