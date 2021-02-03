from abc import ABC, abstractmethod
from typing import Any, Iterable

from treys import Card as TreysCard, Evaluator as TreysEvaluator

from gameframe.poker.utils.cards import Card


class Hand(ABC):
    """Hand is the abstract base class for all hands."""

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class TreysHand(Hand):
    treys_evaluator = TreysEvaluator()

    def __init__(self, hole_cards: Iterable[Card], board_cards: Iterable[Card]):
        self.__hand_rank: int = self.treys_evaluator.evaluate(
            list(map(TreysCard.new, map(lambda card: f'{card.rank.value}{card.suit.value}', hole_cards))),
            list(map(TreysCard.new, map(lambda card: f'{card.rank.value}{card.suit.value}', board_cards))),
        )

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, TreysHand):
            return self.__hand_rank > other.__hand_rank
        else:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TreysHand):
            return self.__hand_rank == other.__hand_rank
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.__hand_rank)

    def __repr__(self) -> str:
        return str(self.treys_evaluator.class_to_string(self.treys_evaluator.get_rank_class(self.__hand_rank)))
