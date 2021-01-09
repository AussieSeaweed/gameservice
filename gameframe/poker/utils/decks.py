from abc import ABC, abstractmethod
from random import shuffle

from gameframe.poker.utils.cards import Card, Rank, Suit


class Deck(ABC):
    """Deck is the abstract base class for all decks."""

    def __init__(self):
        self.__cards = self._create_cards()

        shuffle(self.__cards)

    def draw(self, card_count):
        """Draws a number of cards from the deck.

        :param card_count: the maximum number of cards to be drawn
        :return: a list of drawn cards
        """
        cards = self.peek(card_count)

        del self.__cards[:card_count]

        return cards

    def peek(self, card_count):
        """Peeks a number of cards from the deck.

        :param card_count: the maximum number of cards to be peeked
        :return: a list of peeked cards
        """
        return self.__cards[:card_count]

    @abstractmethod
    def _create_cards(self):
        pass


class StandardDeck(Deck):
    """StandardDeck is the class for standard decks."""

    def _create_cards(self):
        return [Card(rank, suit) for rank in Rank for suit in Suit]


class SixPlusDeck(Deck):
    """SixPlusDeck is the class for six-plus decks."""

    def _create_cards(self):
        return [Card(rank, suit) for rank in Rank if not rank.isdigit() or int(rank) >= 6 for suit in Suit]
