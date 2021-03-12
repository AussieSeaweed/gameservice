from collections.abc import Iterable
from typing import final

from auxiliary import ilen, retain_iter
from pokertools import (Deck, Evaluator, GreekEvaluator, OmahaEvaluator, ShortDeck, ShortEvaluator, StandardDeck,
                        StandardEvaluator)

from gameframe.poker.bases import Limit, Poker
from gameframe.poker.parameters import BettingStage, BoardDealingStage, FixedLimit, HoleDealingStage, NoLimit, PotLimit


class HGame(Poker):
    """HGame is the class for Hold'em games."""

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


class FLHGame(HGame):
    """FLHGame is the class for Fixed-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, FixedLimit(), evaluator, deck, ante, blinds, starting_stacks)


class PLHGame(HGame):
    """PLHGame is the class for Pot-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, PotLimit(), evaluator, deck, ante, blinds, starting_stacks)


class NLHGame(HGame):
    """NLHGame is the class for No-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, NoLimit(), evaluator, deck, ante, blinds, starting_stacks)


@final
class FLTGame(FLHGame):
    """FLTGame is the class for Fixed-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PLTGame(PLHGame):
    """PLTGame is the class for Pot-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NLTGame(NLHGame):
    """NLTGame is the class for No-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLOGame(FLHGame):
    """FLOGame is the class for Fixed-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PLOGame(PLHGame):
    """PLOGame is the class for Pot-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NLOGame(NLHGame):
    """NLOGame is the class for No-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLFCOGame(FLHGame):
    """FLFCOGame is the class for Fixed-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PLFCOGame(PLHGame):
    """PLFCOGame is the class for Pot-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NLFCOGame(NLHGame):
    """NLFCOGame is the class for No-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLSCOGame(FLHGame):
    """FLSCOGame is the class for Fixed-Limit 6-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(6, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PLSCOGame(PLHGame):
    """PLSCOGame is the class for Pot-Limit 6-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(6, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NLSCOGame(NLHGame):
    """NLSCOGame is the class for No-Limit 6-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(6, OmahaEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


class CGame(Poker):
    """CGame is the class for Courchevel games."""

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
class FLCGame(CGame):
    """FLCGame is the class for Fixed-Limit Courchevel games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PLCGame(CGame):
    """PLCGame is the class for Pot-Limit Courchevel games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NLCGame(CGame):
    """NLCGame is the class for No-Limit Courchevel games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


@final
class FLGGame(FLHGame):
    """FLGGame is the class for Fixed-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, GreekEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class PLGGame(PLHGame):
    """PLGGame is the class for Pot-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, GreekEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class NLGGame(NLHGame):
    """NLGGame is the class for No-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, GreekEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLSGame(FLHGame):
    """FLSGame is the class for Fixed-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortEvaluator(), ShortDeck(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class PLSGame(PLHGame):
    """PLSGame is the class for Pot-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortEvaluator(), ShortDeck(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class NLSGame(NLHGame):
    """NLSGame is the class for No-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortEvaluator(), ShortDeck(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)
