from abc import ABC, abstractmethod

from .cards import Card, Rank, Suit


class Deck(ABC):
    """Deck is the abstract base class for all decks."""

    def __init__(self):
        self.__cards = self._create_cards()

    def draw(self, num_cards):
        """Draws a number of cards from the deck.

        :param num_cards: the maximum number of cards to be drawn
        :return: a list of drawn cards
        """
        cards = self.peek(num_cards)

        del self.__cards[:num_cards]

        return cards

    def peek(self, num_cards):
        """Peeks a number of cards from the deck.

        :param num_cards: the maximum number of cards to be peeked
        :return: a list of peeked cards
        """
        return self.__cards[:num_cards]

    @abstractmethod
    def _create_cards(self):
        pass


class StandardDeck(Deck):
    """StandardDeck is the class for standard decks."""

    def _create_cards(self):
        return [Card(rank, suit) for rank in Rank for suit in Suit]
