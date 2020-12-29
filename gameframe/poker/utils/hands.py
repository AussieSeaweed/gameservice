from abc import ABC, abstractmethod

from treys import Card as _TreysCard, Evaluator as _TreysEvaluator


class Hand(ABC):
    """Hand is the abstract base class for all hands."""

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class _TreysHand(Hand):
    __treys_evaluator = _TreysEvaluator()

    def __init__(self, hole_cards, board_cards):
        self.__hand_rank = self.__treys_evaluator.evaluate(list(map(_TreysCard.new, map(str, hole_cards))),
                                                           list(map(_TreysCard.new, map(str, board_cards))))

    def __lt__(self, other):
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other):
        return self.__hand_rank == other.__hand_rank

    def __hash__(self):
        return hash(self.__hand_rank)

    def __str__(self):
        return self.__treys_evaluator.class_to_string(self.__treys_evaluator.get_rank_class(self.__hand_rank))
