from typing import List


class Evaluator52:
    def __init__(self):
        from treys import Evaluator

        self.__evaluator: Evaluator = Evaluator()

    def evaluate(self, card_str_list):
        from treys import Card

        card_int_list: List[int] = [Card.new(card_str) for card_str in card_str_list]

        return self.__evaluator.evaluate(card_int_list, [])
