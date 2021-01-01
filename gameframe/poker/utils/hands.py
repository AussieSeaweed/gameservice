from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TYPE_CHECKING, TypeVar

from treys import Card as _TreysCard, Evaluator as _TreysEvaluator

if TYPE_CHECKING:
    from gameframe.poker import Card

H = TypeVar('H', bound='Hand')


class Hand(Generic[H], ABC):
    """Hand is the abstract base class for all hands."""

    @abstractmethod
    def __lt__(self: H, other: H) -> bool:
        pass

    @abstractmethod
    def __eq__(self: H, other: H) -> bool:
        pass

    @abstractmethod
    def __hash__(self: H) -> int:
        pass

    @abstractmethod
    def __str__(self: H) -> str:
        pass


class _TreysHand(Hand['_TreysHand']):
    __treys_evaluator: _TreysEvaluator = _TreysEvaluator()

    def __init__(self, hole_cards: list[Card], board_cards: list[Card]) -> None:
        self.__hand_rank: int = self.__treys_evaluator.evaluate(list(map(_TreysCard.new, map(str, hole_cards))),
                                                                list(map(_TreysCard.new, map(str, board_cards))))

    def __lt__(self, other: _TreysHand) -> bool:
        return self.__hand_rank > other.__hand_rank

    def __eq__(self, other: _TreysHand) -> bool:
        return self.__hand_rank == other.__hand_rank

    def __hash__(self) -> int:
        return hash(self.__hand_rank)

    def __str__(self) -> str:
        return self.__treys_evaluator.class_to_string(self.__treys_evaluator.get_rank_class(self.__hand_rank))
