from __future__ import annotations

from abc import ABC, abstractmethod

from treys import Card as _TreysCard, Evaluator as _TreysEvaluator

from gameframe.utils.cards import Card


class Hand(ABC):
    """Hand is the abstract base class for all hands."""

    @abstractmethod
    def __lt__(self: Hand, other: Hand) -> bool:
        pass

    @abstractmethod
    def __eq__(self: Hand, other: Hand) -> bool:
        pass

    @abstractmethod
    def __hash__(self: Hand) -> int:
        pass

    @abstractmethod
    def __str__(self: Hand) -> str:
        pass


class _TreysHand(Hand):
    __treys_evaluator: _TreysEvaluator = _TreysEvaluator()

    def __init__(self: _TreysHand, hole_cards: list[Card], board_cards: list[Card]) -> None:
        self.__hand_rank: int = self.__treys_evaluator.evaluate(list(map(_TreysCard.new, map(str, hole_cards))),
                                                                list(map(_TreysCard.new, map(str, board_cards))))

    def __lt__(self: _TreysHand, other: _TreysHand) -> bool:
        return self.__hand_rank > other.__hand_rank

    def __eq__(self: _TreysHand, other: _TreysHand) -> bool:
        return self.__hand_rank == other.__hand_rank

    def __hash__(self: _TreysHand) -> int:
        return hash(self.__hand_rank)

    def __str__(self: _TreysHand) -> str:
        return self.__treys_evaluator.class_to_string(self.__treys_evaluator.get_rank_class(self.__hand_rank))
