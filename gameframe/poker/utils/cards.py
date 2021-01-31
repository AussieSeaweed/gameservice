from enum import Enum
from typing import Any


class Rank(Enum):
    """Rank is the enum for ranks."""
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'


class Suit(Enum):
    """Suit is the enum for suits."""
    CLUB = 'c'
    DIAMOND = 'd'
    HEART = 'h'
    SPADE = 's'


class Card:
    """Card is the base class for all cards."""

    def __init__(self, rank: Rank, suit: Suit):
        self.__rank = rank
        self.__suit = suit

    def __repr__(self) -> str:
        return self.rank.value + self.suit.value

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            ranks, suits = list(Rank), list(Suit)

            if ranks.index(self.__rank) == ranks.index(other.__rank):
                return suits.index(self.__suit) < suits.index(other.__suit)
            else:
                return ranks.index(self.__rank) < ranks.index(other.__rank)
        else:
            raise NotImplemented

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        else:
            raise NotImplemented

    @property
    def rank(self) -> Rank:
        return self.__rank

    @property
    def suit(self) -> Suit:
        return self.__suit


class HoleCard(Card):
    """HoleCard is the class for hole cards."""

    def __init__(self, card: Card, status: bool):
        super().__init__(card.rank, card.suit)

        self._status = status

    def __repr__(self) -> str:
        value = super().__repr__()

        return value if self._status else value + ' (hidden)'

    @property
    def status(self) -> bool:
        return self._status
