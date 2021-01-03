from __future__ import annotations

from abc import ABC
from typing import Sequence, TYPE_CHECKING, final

from gameframe.poker.bases import PokerGame
from gameframe.poker.limits import NoLimit
from gameframe.poker.rounds import BettingRound
from gameframe.poker.utils import GreekHoldEmEvaluator, OmahaHoldEmEvaluator, StandardDeck, StandardEvaluator

if TYPE_CHECKING:
    from gameframe.poker import Deck, Evaluator, Limit


class HoldEmGame(PokerGame, ABC):
    """HoldEmGame is the abstract base class for all hold'em games."""

    def __init__(self, deck: Deck, evaluator: Evaluator, limit: Limit, hole_card_count: int,
                 board_card_counts: Sequence[int], ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int], lazy: bool) -> None:
        super().__init__(deck, evaluator, limit, [BettingRound(self, 0, [False] * hole_card_count)] + list(map(
            lambda board_card_count: BettingRound(self, board_card_count, []),
            board_card_counts,
        )), ante, blinds, starting_stacks, lazy)


class TexasHoldEmGame(HoldEmGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def __init__(self, limit: Limit, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int],
                 lazy: bool) -> None:
        super().__init__(StandardDeck(), StandardEvaluator(), limit, 2, [3, 1, 1], ante, blinds, starting_stacks, lazy)


@final
class NoLimitTexasHoldEmGame(TexasHoldEmGame, ABC):
    """NoLimitTexasHoldEmGame is the abstract base class for all no-limit texas hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int], lazy: bool) -> None:
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, lazy)


class GreekHoldEmGame(HoldEmGame, ABC):
    """GreekHoldEmGame is the abstract base class for all greek hold'em games."""

    def __init__(self, limit: Limit, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int],
                 lazy: bool) -> None:
        super().__init__(StandardDeck(), GreekHoldEmEvaluator(), limit, 2, [3, 1, 1], ante, blinds, starting_stacks,
                         lazy)


@final
class NoLimitGreekHoldEmGame(GreekHoldEmGame, ABC):
    """NoLimitGreekHoldEmGame is the abstract base class for all no-limit greek hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int], lazy: bool) -> None:
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, lazy)


class OmahaHoldEmGame(HoldEmGame, ABC):
    """OmahaHoldEmGame is the abstract base class for all omaha hold'em games."""

    def __init__(self, limit: Limit, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int],
                 lazy: bool) -> None:
        super().__init__(StandardDeck(), OmahaHoldEmEvaluator(), limit, 4, [3, 1, 1], ante, blinds, starting_stacks,
                         lazy)


@final
class NoLimitOmahaHoldEmGame(OmahaHoldEmGame, ABC):
    """NoLimitOmahaHoldEmGame is the abstract base class for all no-limit omaha hold'em games."""

    def __init__(self, ante: int, blinds: Sequence[int], starting_stacks: Sequence[int], lazy: bool) -> None:
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, lazy)
