from collections.abc import Iterable
from typing import final

from auxiliary import ilen, retain_iter
from pokertools import (Deck, Evaluator, GreekEvaluator, OmahaEvaluator, ShortDeck, ShortEvaluator, StandardDeck,
                        StandardEvaluator)

from gameframe.poker.bases import Limit, Poker
from gameframe.poker.parameters import BettingStage, BoardDealingStage, FixedLimit, HoleDealingStage, NoLimit, PotLimit


class HoldEm(Poker):
    """HoldEm is the class for Hold'em games."""

    @retain_iter
    def __init__(self, hole_card_count: int, limit: Limit, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(hole_card_count, False), BettingStage(max_delta),
            BoardDealingStage(3), BettingStage(max_delta),
            BoardDealingStage(1), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            BoardDealingStage(1), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, evaluator, deck, ante, blinds, starting_stacks)


class FixedLimitHoldEm(HoldEm):
    """FixedLimitHoldEm is the class for Fixed-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, FixedLimit(), evaluator, deck, ante, blinds, starting_stacks)


class PotLimitHoldEm(HoldEm):
    """PotLimitHoldEm is the class for Pot-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, PotLimit(), evaluator, deck, ante, blinds, starting_stacks)


class NoLimitHoldEm(HoldEm):
    """NoLimitHoldEm is the class for No-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, NoLimit(), evaluator, deck, ante, blinds, starting_stacks)


@final
class FixedLimitTexasHoldEm(FixedLimitHoldEm):
    """FixedLimitTexasHoldEm is the class for Fixed-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PotLimitTexasHoldEm(PotLimitHoldEm):
    """PotLimitTexasHoldEm is the class for Pot-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NoLimitTexasHoldEm(NoLimitHoldEm):
    """NoLimitTexasHoldEm is the class for No-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitOmahaHoldEm(FixedLimitHoldEm):
    """FixedLimitOmahaHoldEm is the class for Fixed-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PotLimitOmahaHoldEm(PotLimitHoldEm):
    """PotLimitOmahaHoldEm is the class for Pot-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NoLimitOmahaHoldEm(NoLimitHoldEm):
    """NoLimitOmahaHoldEm is the class for No-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitFiveCardOmahaHoldEm(FixedLimitHoldEm):
    """FixedLimitFiveCardOmahaHoldEm is the class for Fixed-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PotLimitFiveCardOmahaHoldEm(PotLimitHoldEm):
    """PotLimitFiveCardOmahaHoldEm is the class for Pot-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NoLimitFiveCardOmahaHoldEm(NoLimitHoldEm):
    """NoLimitFiveCardOmahaHoldEm is the class for No-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitSixCardOmahaHoldEm(FixedLimitHoldEm):
    """FixedLimitSixCardOmahaHoldEm is the class for Fixed-Limit 6-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(6, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PotLimitSixCardOmahaHoldEm(PotLimitHoldEm):
    """PotLimitSixCardOmahaHoldEm is the class for Pot-Limit 6-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(6, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NoLimitSixCardOmahaHoldEm(NoLimitHoldEm):
    """NoLimitSixCardOmahaHoldEm is the class for No-Limit 6-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(6, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


class Courchevel(Poker):
    """Courchevel is the class for Courchevel games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(5, False), BoardDealingStage(1), BettingStage(max_delta),
            BoardDealingStage(2), BettingStage(max_delta),
            BoardDealingStage(1), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            BoardDealingStage(1), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitCourchevel(Courchevel):
    """FixedLimitCourchevel is the class for Fixed-Limit Courchevel games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PotLimitCourchevel(Courchevel):
    """PotLimitCourchevel is the class for Pot-Limit Courchevel games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NoLimitCourchevel(Courchevel):
    """NoLimitCourchevel is the class for No-Limit Courchevel games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


@final
class FixedLimitGreekHoldEm(FixedLimitHoldEm):
    """FixedLimitGreekHoldEm is the class for Fixed-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, GreekEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PotLimitGreekHoldEm(PotLimitHoldEm):
    """PotLimitGreekHoldEm is the class for Pot-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, GreekEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NoLimitGreekHoldEm(NoLimitHoldEm):
    """NoLimitGreekHoldEm is the class for No-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, GreekEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitShortHoldEm(FixedLimitHoldEm):
    """FixedLimitShortHoldEm is the class for Fixed-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortEvaluator(), ShortDeck(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class PotLimitShortHoldEm(PotLimitHoldEm):
    """PotLimitShortHoldEm is the class for Pot-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortEvaluator(), ShortDeck(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class NoLimitShortHoldEm(NoLimitHoldEm):
    """NoLimitShortHoldEm is the class for No-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortEvaluator(), ShortDeck(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)
