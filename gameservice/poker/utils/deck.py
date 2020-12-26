"""
This module defines decks in gameservice.
"""
from abc import ABC, abstractmethod

from .card import Card
from .treys_utils import create_standard_deck


class Deck(ABC):
    """
    This is a class that represents decks.
    """

    @abstractmethod
    def draw(self, num_cards):
        """
        Draws a number of cards from the deck.

        :param num_cards: the number of cards to be drawn
        :return: a list of drawn cards
        """
        pass

    @abstractmethod
    def peek(self, num_cards):
        """
        Peeks a number of cards from the deck.

        :param num_cards: the number of cards to be peeked
        :return: a list of peeked cards
        """
        pass


class StandardDeck(Deck):
    """
    This is a class that represents standard decks.
    """

    def __init__(self):
        self.__deck = create_standard_deck()

    def draw(self, num_cards):
        cards = list(map(Card, self.__deck[:num_cards]))

        del self.__deck[:num_cards]

        return cards

    def peek(self, num_cards):
        return list(map(Card, self.__deck.cards[:num_cards]))
