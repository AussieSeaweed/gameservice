from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from treys import Card as TreysCard, Evaluator as TreysEvaluator

from .cards import Card

H = TypeVar('H')  # TODO: BOUND HAND TYPES AS SEQUENTIAL AND GAME


class Hand(Generic[H], ABC):
    """Hand is the abstract base class for all hands."""

    @abstractmethod
    def __lt__(self, other: H) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other: H) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class _TreysHand(Hand['_TreysHand']):
    __treys_evaluator = TreysEvaluator()

    def __init__(self, hole_cards: List[Card], board_cards: List[Card]):
        self.__hand_rank: int = self.__treys_evaluator.evaluate(list(map(TreysCard.new, map(str, hole_cards))),
                                                                list(map(TreysCard.new, map(str, board_cards))))

    def __lt__(self, other: _TreysHand) -> bool:
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other: _TreysHand) -> bool:
        return self.__hand_rank == other.__hand_rank

    def __hash__(self) -> int:
        return hash(self.__hand_rank)

    def __str__(self) -> str:
        return self.__treys_evaluator.class_to_string(self.__treys_evaluator.get_rank_class(self.__hand_rank))
