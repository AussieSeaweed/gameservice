from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, final

from gameframe.poker.utils.cards import Card, Rank, Suit
from gameframe.utils import override


class Deck(ABC):
    """Deck is the abstract base class for all decks."""

    def __init__(self) -> None:
        self.__cards: list[Card] = self._create_cards()

    @final
    def draw(self, card_count: int) -> Sequence[Card]:
        """Draws a number of cards from the deck.

        :param card_count: the maximum number of cards to be drawn
        :return: a list of drawn cards
        """
        cards: Sequence[Card] = self.peek(card_count)

        del self.__cards[:card_count]

        return cards

    @final
    def peek(self, card_count: int) -> Sequence[Card]:
        """Peeks a number of cards from the deck.

        :param card_count: the maximum number of cards to be peeked
        :return: a list of peeked cards
        """
        return self.__cards[:card_count]

    @abstractmethod
    def _create_cards(self) -> list[Card]:
        pass


@final
class StandardDeck(Deck):
    """StandardDeck is the class for standard decks."""

    @override
    def _create_cards(self) -> list[Card]:
        return [Card(rank, suit) for rank in Rank for suit in Suit]


@final
class SixPlusDeck(Deck):
    """SixPlusDeck is the class for six-plus decks."""

    @override
    def _create_cards(self) -> list[Card]:
        return [Card(rank, suit) for rank in Rank if not rank.isdigit() or int(rank) >= 6 for suit in Suit]
