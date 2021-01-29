from abc import ABC, abstractmethod
from random import shuffle
from typing import Iterable, Iterator
from typing import MutableSequence

from gameframe.poker.utils.cards import Card, Rank, Suit


class Deck(Iterable[Card], ABC):
    """Deck is the abstract base class for all decks."""

    def __init__(self) -> None:
        self.__cards = self._create_cards()

        shuffle(self.__cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self.__cards)

    def remove(self, cards: Iterable[Card]) -> None:
        """Removes the cards from the deck.

        :param cards: the cards to be removed
        :return: a list of drawn cards
        """
        for card in cards:
            self.__cards.remove(card)

    @abstractmethod
    def _create_cards(self) -> MutableSequence[Card]:
        pass


class StandardDeck(Deck):
    """StandardDeck is the class for standard decks."""

    def _create_cards(self) -> MutableSequence[Card]:
        return [Card(rank, suit) for rank in Rank for suit in Suit]


class SixPlusDeck(Deck):
    """SixPlusDeck is the class for six-plus decks."""

    def _create_cards(self) -> MutableSequence[Card]:
        return [
            Card(rank, suit) for rank in Rank
            if not str(rank).isdigit() or int(str(rank)) >= 6 for suit in Suit
        ]
