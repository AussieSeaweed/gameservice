from abc import ABC
from collections import Sequence
from typing import final

from pokertools import (Deck, Evaluator, GreekEvaluator, OmahaEvaluator, ShortDeck, ShortEvaluator, StandardDeck,
                        StandardEvaluator)

from gameframe.poker._stages import (BettingStage, BoardCardDealingStage, HoleCardDealingStage, NLBettingStage,
                                     PLBettingStage, ShowdownStage)
from gameframe.poker.bases import PokerGame


class HEGame(PokerGame, ABC):
    """HEGame is the class for Hold'em games."""

    def __init__(self, pre_flop: BettingStage, flop: BettingStage, turn: BettingStage, river: BettingStage,
                 hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        super().__init__([
            HoleCardDealingStage(self, hole_card_count, False), pre_flop,
            BoardCardDealingStage(self, 3), flop,
            BoardCardDealingStage(self, 1), turn,
            BoardCardDealingStage(self, 1), river,
            ShowdownStage(self),
        ], deck, evaluator, ante, blinds, starting_stacks)


class NLHEGame(HEGame, ABC):
    """NLHEGame is the class for No-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__(
            NLBettingStage(self, max_delta), NLBettingStage(self, max_delta), NLBettingStage(self, max_delta),
            NLBettingStage(self, max_delta), hole_card_count, deck, evaluator, ante, blinds, starting_stacks,
        )


class PLHEGame(HEGame, ABC):
    """PLHEGame is the class for Pot-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        max_delta = max(ante, max(blinds))

        super().__init__(
            PLBettingStage(self, max_delta), PLBettingStage(self, max_delta), PLBettingStage(self, max_delta),
            PLBettingStage(self, max_delta), hole_card_count, deck, evaluator, ante, blinds, starting_stacks,
        )


@final
class NLTGame(NLHEGame):
    """NLTGame is the class for No-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class NLOGame(NLHEGame):
    """NLOGame is the class for No-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class NLGGame(NLHEGame):
    """NLGGame is the class for No-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class NLSGame(NLHEGame):
    """NLSGame is the class for No-Limit Short-Deck Hold'em games."""

    def __init__(self, ante: int, button_blind: int, starting_stacks: Sequence[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, [0] * (len(starting_stacks) - 1) + [button_blind],
                         starting_stacks)


@final
class PLTGame(PLHEGame):
    """PLTGame is the class for Pot-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class PLOGame(PLHEGame):
    """PLOGame is the class for Pot-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class PLGGame(PLHEGame):
    """PLGGame is the class for Pot-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class PLSGame(PLHEGame):
    """PLSGame is the class for Pot-Limit Short-Deck Hold'em games."""

    def __init__(self, ante: int, button_blind: int, starting_stacks: Sequence[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, [0] * (len(starting_stacks) - 1) + [button_blind],
                         starting_stacks)
