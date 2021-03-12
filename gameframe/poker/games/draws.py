from collections.abc import Iterable
from typing import final

from auxiliary import retain_iter
from pokertools import (BadugiEvaluator, Card, Deck, Lowball27Evaluator, Rank, RankEvaluator, StandardDeck,
                        StandardEvaluator, Suit)

from gameframe.poker.bases import Limit, Poker
from gameframe.poker.parameters import (BettingStage, DrawStage, FixedLimit, HoleDealingStage,
                                        NoLimit, PotLimit)


class FCDGame(Poker):
    """FCDGame is the base class for all Five-Card Draw games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((HoleDealingStage(5, False), BettingStage(max_delta), DrawStage(), BettingStage(max_delta)),
                         limit, StandardEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLFCDGame(FCDGame):
    """FLFCDGame is the class for Fixed-Limit Five-Card Draw games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PLFCDGame(FCDGame):
    """PLFCDGame is the class for Pot-Limit Five-Card Draw games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NLFCDGame(FCDGame):
    """NLFDGame is the class for No-Limit Five-Card Draw games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


class BGame(Poker):
    """BGame is the class for Badugi games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(4, False), BettingStage(max_delta),
            DrawStage(), BettingStage(max_delta),
            DrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            DrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, BadugiEvaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLBGame(BGame):
    """FLBGame is the class for Fixed-Limit Badugi games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PLBGame(BGame):
    """PLBGame is the class for Pot-Limit Badugi games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NLBGame(BGame):
    """NLBGame is the class for No-Limit Badugi games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


class SDLB27Game(Poker):
    """SDLB27Game is the class for 2-7 Single Draw Lowball games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((HoleDealingStage(5, False), BettingStage(max_delta), DrawStage(), BettingStage(max_delta)),
                         limit, Lowball27Evaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLSDLB27Game(SDLB27Game):
    """FLSDLB27Game is the class for Fixed-Limit 2-7 Single Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PLSDLB27Game(SDLB27Game):
    """PLSDLB27Game is the class for Pot-Limit 2-7 Single Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NLSDLB27Game(SDLB27Game):
    """NLSDLB27Game is the class for No-Limit 2-7 Single Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


class TDLB27Game(Poker):
    """TDLB27Game is the class for 2-7 Triple Draw Lowball games."""

    @retain_iter
    def __init__(self, limit: Limit, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        max_delta = max(ante, max(blinds))

        super().__init__((
            HoleDealingStage(5, False), BettingStage(max_delta),
            DrawStage(), BettingStage(max_delta),
            DrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
            DrawStage(), BettingStage(2 * max_delta if isinstance(limit, FixedLimit) else max_delta),
        ), limit, Lowball27Evaluator(), StandardDeck(), ante, blinds, starting_stacks)


@final
class FLTDLB27Game(SDLB27Game):
    """FLTDLB27Game is the class for Fixed-Limit 2-7 Triple Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(FixedLimit(), ante, blinds, starting_stacks)


@final
class PLTDLB27Game(SDLB27Game):
    """PLTDLB27Game is the class for Pot-Limit 2-7 Triple Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(PotLimit(), ante, blinds, starting_stacks)


@final
class NLTDLB27Game(SDLB27Game):
    """NLTDLB27Game is the class for No-Limit 2-7 Triple Draw Lowball games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(NoLimit(), ante, blinds, starting_stacks)


@final
class KuhnGame(Poker):
    """KuhnGame is the class for Kuhn Poker games."""

    def __init__(self) -> None:
        super().__init__((HoleDealingStage(1, False), BettingStage(1)), FixedLimit(), RankEvaluator(), Deck(
            (Card(Rank.JACK, Suit.SPADE), Card(Rank.QUEEN, Suit.SPADE), Card(Rank.KING, Suit.SPADE))
        ), 1, (), (2, 2))
