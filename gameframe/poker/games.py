from abc import ABC
from collections.abc import Iterable
from typing import final

from auxiliary import ilen, retain_iter
from pokertools import (Card, Deck, Evaluator, GreekEvaluator, OmahaEvaluator, Rank, ShortDeck, ShortEvaluator,
                        StandardDeck, StandardEvaluator, Suit)
from pokertools.evaluators import RankEvaluator

from gameframe.poker.bases import Limit, PokerGame
from gameframe.poker.params import BettingStage, BoardDealingStage, FixedLimit, HoleDealingStage, NoLimit, PotLimit


class HGame(PokerGame, ABC):
    """HGame is the class for Hold'em games."""

    @retain_iter
    def __init__(self, hole_card_count: int, limit: Limit, deck: Deck, evaluator: Evaluator,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(hole_card_count, False), BettingStage(max_delta),
            BoardDealingStage(3), BettingStage(max_delta),
            BoardDealingStage(1), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            BoardDealingStage(1), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, evaluator, deck, ante, blinds, starting_stacks)


class FLHGame(HGame, ABC):
    """FLHGame is the class for Fixed-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, FixedLimit(), deck, evaluator, ante, blinds, starting_stacks)


class PLHGame(HGame, ABC):
    """PLHGame is the class for Pot-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, PotLimit(), deck, evaluator, ante, blinds, starting_stacks)


class NLHGame(HGame, ABC):
    """NLHGame is the class for No-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator,
                 ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(hole_card_count, NoLimit(), deck, evaluator, ante, blinds, starting_stacks)


@final
class FLTGame(FLHGame):
    """FLTGame is the class for Fixed-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class PLTGame(PLHGame):
    """PLTGame is the class for Pot-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class NLTGame(NLHGame):
    """NLTGame is the class for No-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class FLOGame(FLHGame):
    """FLOGame is the class for Fixed-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class PLOGame(PLHGame):
    """PLOGame is the class for Pot-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class NLOGame(NLHGame):
    """NLOGame is the class for No-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class FL5OGame(FLHGame):
    """FL5OGame is the class for Fixed-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class PL5OGame(PLHGame):
    """PL5OGame is the class for Pot-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class NL5OGame(NLHGame):
    """NL5OGame is the class for No-Limit 5-Card Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(5, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class FLGGame(FLHGame):
    """FLGGame is the class for Fixed-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class PLGGame(PLHGame):
    """PLGGame is the class for Pot-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class NLGGame(NLHGame):
    """NLGGame is the class for No-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class FLSGame(FLHGame):
    """FLSGame is the class for Fixed-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class PLSGame(PLHGame):
    """PLSGame is the class for Pot-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class NLSGame(NLHGame):
    """NLSGame is the class for No-Limit Short-Deck Hold'em games."""

    @retain_iter
    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        super().__init__(2, ShortDeck(), ShortEvaluator(), ante, (0,) * (ilen(starting_stacks) - 1) + (button_blind,),
                         starting_stacks)


@final
class KuhnGame(PokerGame):
    """KuhnGame is the class for Kuhn Poker games."""

    def __init__(self) -> None:
        super().__init__((HoleDealingStage(1, False), BettingStage(1)), FixedLimit(), RankEvaluator(), Deck(
            (Card(Rank.JACK, Suit.SPADE), Card(Rank.QUEEN, Suit.SPADE), Card(Rank.KING, Suit.SPADE))
        ), 1, (), (2, 2))
