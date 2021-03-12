from collections.abc import Iterable
from typing import final

from auxiliary import retain_iter
from pokertools import (BadugiEvaluator, Card, Deck, Lowball27Evaluator, Rank, RankEvaluator, StandardDeck,
                        StandardEvaluator, Suit)

from gameframe.poker.bases import Limit, Poker
from gameframe.poker.parameters import BettingStage, DiscardDrawStage, FixedLimit, HoleDealingStage, NoLimit, PotLimit


class FiveCardDraw(Poker):
    """FiveCardDraw is the base class for all Five-Card Draw games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__(
            (HoleDealingStage(5, False), BettingStage(max_delta), DiscardDrawStage(), BettingStage(max_delta)),
            limit, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks,
        )


@final
class FixedLimitFiveCardDraw(FiveCardDraw):
    """FixedLimitFiveCardDraw is the class for Fixed-Limit Five-Card Draw games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PotLimitFiveCardDraw(FiveCardDraw):
    """PotLimitFiveCardDraw is the class for Pot-Limit Five-Card Draw games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NoLimitFiveCardDraw(FiveCardDraw):
    """NoLimitFiveCardDraw is the class for No-Limit Five-Card Draw games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


class Badugi(Poker):
    """Badugi is the class for Badugi games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(4, False), BettingStage(max_delta),
            DiscardDrawStage(), BettingStage(max_delta),
            DiscardDrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            DiscardDrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, BadugiEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitBadugi(Badugi):
    """FixedLimitBadugi is the class for Fixed-Limit Badugi games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PotLimitBadugi(Badugi):
    """PotLimitBadugi is the class for Pot-Limit Badugi games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NoLimitBadugi(Badugi):
    """NoLimitBadugi is the class for No-Limit Badugi games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


class SingleDrawLowball27(Poker):
    """SingleDrawLowball27 is the class for 2-7 Single Draw Lowball games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__(
            (HoleDealingStage(5, False), BettingStage(max_delta), DiscardDrawStage(), BettingStage(max_delta)),
            limit, Lowball27Evaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitSingleDrawLowball27(SingleDrawLowball27):
    """FixedLimitSingleDrawLowball27 is the class for Fixed-Limit 2-7 Single Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PotLimitSingleDrawLowball27(SingleDrawLowball27):
    """PotLimitSingleDrawLowball27 is the class for Pot-Limit 2-7 Single Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NoLimitSingleDrawLowball27(SingleDrawLowball27):
    """NoLimitSingleDrawLowball27 is the class for No-Limit 2-7 Single Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


class TripleDrawLowball27(Poker):
    """TripleDrawLowball27 is the class for 2-7 Triple Draw Lowball games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(5, False), BettingStage(max_delta),
            DiscardDrawStage(), BettingStage(max_delta),
            DiscardDrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            DiscardDrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, Lowball27Evaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FixedLimitTripleDrawLowball27(SingleDrawLowball27):
    """FixedLimitTripleDrawLowball27 is the class for Fixed-Limit 2-7 Triple Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PotLimitTripleDrawLowball27(SingleDrawLowball27):
    """PotLimitTripleDrawLowball27 is the class for Pot-Limit 2-7 Triple Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NoLimitTripleDrawLowball27(SingleDrawLowball27):
    """NoLimitTripleDrawLowball27 is the class for No-Limit 2-7 Triple Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


@final
class KuhnPoker(Poker):
    """KuhnPoker is the class for Kuhn Poker games."""

    def __init__(self) -> None:
        super().__init__((HoleDealingStage(1, False), BettingStage(1)), FixedLimit(), RankEvaluator(), Deck(
            (Card(Rank.JACK, Suit.SPADE), Card(Rank.QUEEN, Suit.SPADE), Card(Rank.KING, Suit.SPADE))
        ), 1, (), (2, 2))
