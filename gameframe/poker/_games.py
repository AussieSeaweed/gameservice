from abc import ABC
from collections import Iterable, Sequence
from typing import final

from pokertools import (Card, Deck, Evaluator, GreekEvaluator, OmahaEvaluator, Rank, ShortDeck, ShortEvaluator,
                        StandardDeck, StandardEvaluator, Suit)
from pokertools.evaluators import RankEvaluator

from gameframe.poker._bases import PokerGame
from gameframe.poker._stages import (BettingStage, BoardCardDealingStage, HoleCardDealingStage, NLBettingStage,
                                     PLBettingStage, ShowdownStage)


class HEGame(PokerGame, ABC):
    """HEGame is the class for Hold'em games."""

    def __init__(
            self, pre_flop: BettingStage, flop: BettingStage, turn: BettingStage, river: BettingStage,
            hole_card_count: int, deck: Deck, evaluator: Evaluator,
            ante: int, blinds: Iterable[int], starting_stacks: Iterable[int],
    ):
        super().__init__([
            HoleCardDealingStage(self, hole_card_count, False), pre_flop,
            BoardCardDealingStage(self, 3), flop,
            BoardCardDealingStage(self, 1), turn,
            BoardCardDealingStage(self, 1), river,
            ShowdownStage(self),
        ], deck, evaluator, ante, blinds, starting_stacks)


class NLHEGame(HEGame, ABC):
    """NLHEGame is the class for No-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Iterable[int],
                 starting_stacks: Iterable[int]):
        d = max(ante, max(blinds := tuple(blinds)))

        super().__init__(
            NLBettingStage(self, d), NLBettingStage(self, d), NLBettingStage(self, d), NLBettingStage(self, d),
            hole_card_count, deck, evaluator, ante, blinds, starting_stacks,
        )


class PLHEGame(HEGame, ABC):
    """PLHEGame is the class for Pot-Limit Hold'em games."""

    def __init__(self, hole_card_count: int, deck: Deck, evaluator: Evaluator, ante: int, blinds: Iterable[int],
                 starting_stacks: Iterable[int]):
        d = max(ante, max(blinds := tuple(blinds)))

        super().__init__(
            PLBettingStage(self, d), PLBettingStage(self, d), PLBettingStage(self, d), PLBettingStage(self, d),
            hole_card_count, deck, evaluator, ante, blinds, starting_stacks,
        )


@final
class NLTGame(NLHEGame):
    """NLTGame is the class for No-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class PLTGame(PLHEGame):
    """PLTGame is the class for Pot-Limit Texas Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), StandardEvaluator(), ante, blinds, starting_stacks)


@final
class NLOGame(NLHEGame):
    """NLOGame is the class for No-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class PLOGame(PLHEGame):
    """PLOGame is the class for Pot-Limit Omaha Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(4, StandardDeck(), OmahaEvaluator(), ante, blinds, starting_stacks)


@final
class NLGGame(NLHEGame):
    """NLGGame is the class for No-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class PLGGame(PLHEGame):
    """PLGGame is the class for Pot-Limit Greek Hold'em games."""

    def __init__(self, ante: int, blinds: Iterable[int], starting_stacks: Iterable[int]):
        super().__init__(2, StandardDeck(), GreekEvaluator(), ante, blinds, starting_stacks)


@final
class NLSGame(NLHEGame):
    """NLSGame is the class for No-Limit Short-Deck Hold'em games."""

    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        if isinstance(starting_stacks, Sequence):
            super().__init__(2, ShortDeck(), ShortEvaluator(), ante, [0] * (len(starting_stacks) - 1) + [button_blind],
                             starting_stacks)
        else:
            NLSGame.__init__(self, ante, button_blind, tuple(starting_stacks))


@final
class PLSGame(PLHEGame):
    """PLSGame is the class for Pot-Limit Short-Deck Hold'em games."""

    def __init__(self, ante: int, button_blind: int, starting_stacks: Iterable[int]):
        if isinstance(starting_stacks, Sequence):
            super().__init__(2, ShortDeck(), ShortEvaluator(), ante, [0] * (len(starting_stacks) - 1) + [button_blind],
                             starting_stacks)
        else:
            PLSGame.__init__(self, ante, button_blind, tuple(starting_stacks))


@final
class KuhnGame(PokerGame):
    def __init__(self) -> None:
        super().__init__(
            (HoleCardDealingStage(self, 1, False), NLBettingStage(self, 1), ShowdownStage(self)),
            Deck((Card(Rank.JACK, Suit.SPADE), Card(Rank.QUEEN, Suit.SPADE), Card(Rank.KING, Suit.SPADE))),
            RankEvaluator(), 1, (), (2, 2),
        )
