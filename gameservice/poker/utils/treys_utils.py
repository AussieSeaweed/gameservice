from treys.evaluator import Evaluator
from treys.deck import Deck
from treys.card import Card

evaluator = Evaluator()


def evaluate(card_strs):
    return evaluator.evaluate(list(map(Card.new, card_strs)), [])


def create_standard_deck():
    return list(map(Card.int_to_str, Deck().cards))


def rank_to_str(hand_rank):
    return evaluator.class_to_string(evaluator.get_rank_class(hand_rank))
