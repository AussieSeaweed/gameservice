from typing import List

from treys import Card, Evaluator

evaluator: Evaluator = Evaluator()


def evaluate52(card_str_list: List[str]) -> int:
    card_int_list: List[int] = [Card.new(card_str) for card_str in card_str_list]

    return evaluator.evaluate(card_int_list, [])
