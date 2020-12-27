from treys.card import Card
from treys.deck import Deck
from treys.evaluator import Evaluator
from itertools import combinations

evaluator = Evaluator()


def evaluate(hole_cards, board):
    """
    Evaluates a hand with respect to hole_cards and board

    :param hole_cards: a list of the hole cards
    :param board: a list of board cards
    :return: a hand rank
    """
    board = list(map(Card.new, board))

    hand_rank = None

    for cards in combinations(list(map(Card.new, hole_cards)), 2):
        if hand_rank is None:
            hand_rank = evaluator.evaluate(list(cards), board)
        else:
            hand_rank = min(hand_rank, evaluator.evaluate(list(cards), board))

    return hand_rank


def create_standard_deck():
    return list(map(Card.int_to_str, Deck().cards))


def rank_to_str(hand_rank):
    return evaluator.class_to_string(evaluator.get_rank_class(hand_rank))
