from abc import ABC, abstractmethod

from treys import Card as TreysCard, Evaluator as TreysEvaluator


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


class TreysHand(Hand):
    treys_evaluator = TreysEvaluator()

    def __init__(self, hole_cards, board_cards):
        self.__hand_rank = self.treys_evaluator.evaluate(list(map(TreysCard.new, map(str, hole_cards))),
                                                         list(map(TreysCard.new, map(str, board_cards))))

    def __lt__(self, other):
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other):
        return self.__hand_rank == other.__hand_rank

    def __hash__(self):
        return hash(self.__hand_rank)

    def __str__(self):
        return self.treys_evaluator.class_to_string(self.treys_evaluator.get_rank_class(self.__hand_rank))
