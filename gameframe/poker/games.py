from abc import ABC
from collections import Sequence
from typing import final

from pokertools import (Deck, Evaluator, GreekEvaluator, OmahaEvaluator, ShortDeck, ShortEvaluator, StandardDeck,
                        StandardEvaluator)

from gameframe.poker._stages import (BettingStage, BoardCardDealingStage, HoleCardDealingStage, NLBettingStage,
                                     PLBettingStage, ShowdownStage)
from gameframe.poker.bases import PokerGame


class HEGame(PokerGame, ABC):
    """HEGame is the class for hold'em games."""

    def __init__(self, pre_flop: BettingStage, flop: BettingStage, turn: BettingStage, river: BettingStage,
                 hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        super().__init__([
            HoleCardDealingStage(self, hole_card_count, False), pre_flop,
            BoardCardDealingStage(self, 3), flop,  # Flop
            BoardCardDealingStage(self, 1), turn,  # Turn
            BoardCardDealingStage(self, 1), river,  # River
            ShowdownStage(self),  # Showdown
        ], deck, evaluator, ante, blinds, starting_stacks)


class NLHEGame(HEGame, ABC):
    """NLHEGame is the class for no-limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__(
            NLBettingStage(self, max_delta), NLBettingStage(self, max_delta), NLBettingStage(self, max_delta),
            NLBettingStage(self, max_delta), hole_card_count, deck, evaluator, ante, blinds, starting_stacks,
        )


class PLHEGame(HEGame, ABC):
    """PLHEGame is the class for pot-limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__(
            PLBettingStage(self, max_delta), PLBettingStage(self, max_delta), PLBettingStage(self, max_delta),
            PLBettingStage(self, max_delta), hole_card_count, deck, evaluator, ante, blinds, starting_stacks,
        )


@final
class NLTGame(NLHEGame):
    """NLTGame is the class for no-limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class NLOGame(NLHEGame):
    """NLOGame is the class for no-limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class NLGGame(NLHEGame):
    """NLGGame is the class for no-limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class NLSGame(NLHEGame):
    """NLSGame is the class for no-limit Short-Deck Hold'em games."""

    def __init__(self, ante: int, blind: int, starting_stacks: Sequence[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, [0] * len(starting_stacks) + [blind], starting_stacks)


@final
class PLTGame(PLHEGame):
    """PLTGame is the class for pot-limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class PLOGame(PLHEGame):
    """PLOGame is the class for pot-limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class PLGGame(PLHEGame):
    """PLGGame is the class for pot-limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class PLSGame(PLHEGame):
    """PLSGame is the class for pot-limit Short-Deck Hold'em games."""

    def __init__(self, ante: int, blind: int, starting_stacks: Sequence[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, [0] * len(starting_stacks) + [blind], starting_stacks)
