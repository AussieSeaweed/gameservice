from __future__ import annotations

from abc import ABC, abstractmethod

from gameframe.utils.cards import Card, Rank, Suit


class Deck(ABC):
    """Deck is the abstract base class for all decks."""

    def __init__(self: Deck) -> None:
        self.__cards: list[Card] = self._create_cards()

    def draw(self: Deck, card_count: int) -> list[Card]:
        """Draws a number of cards from the deck.

        :param card_count: the maximum number of cards to be drawn
        :return: a list of drawn cards
        """
        cards: list[Card] = self.peek(card_count)

        del self.__cards[:card_count]

        return cards

    def peek(self: Deck, card_count: int) -> list[Card]:
        """Peeks a number of cards from the deck.

        :param card_count: the maximum number of cards to be peeked
        :return: a list of peeked cards
        """
        return self.__cards[:card_count]

    @abstractmethod
    def _create_cards(self: Deck) -> list[Card]:
        pass


class StandardDeck(Deck):
    """StandardDeck is the class for standard decks."""

    def _create_cards(self: StandardDeck) -> list[Card]:
        return [Card(rank, suit) for rank in Rank for suit in Suit]


class SixPlusDeck(Deck):
    """SixPlusDeck is the class for six-plus decks."""

    def _create_cards(self: SixPlusDeck) -> list[Card]:
        return [Card(rank, suit) for rank in Rank if not rank.isdigit() or int(rank) >= 6 for suit in Suit]
