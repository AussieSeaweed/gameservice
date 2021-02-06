from enum import Enum, unique
from typing import Any, Union


@unique
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

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Rank):
            ranks = list(Rank)

            return ranks.index(self) < ranks.index(other)
        else:
            return NotImplemented


@unique
class Suit(Enum):
    """Suit is the enum for suits."""
    CLUB = 'c'
    DIAMOND = 'd'
    HEART = 'h'
    SPADE = 's'

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Suit):
            suits = list(Suit)

            return suits.index(self) < suits.index(other)
        else:
            return NotImplemented


class Card:
    """Card is the base class for all cards."""

    def __init__(self, rank: Rank, suit: Suit):
        self.__rank = rank
        self.__suit = suit

    def __repr__(self) -> str:
        return self.rank.value + self.suit.value

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.__suit < other.__suit if self.__rank == other.__rank else self.__rank < other.__rank
        else:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.rank) ^ hash(self.suit)

    @property
    def rank(self) -> Rank:
        """
        :return: the rank of this card
        """
        return self.__rank

    @property
    def suit(self) -> Suit:
        """
        :return: the suit of this card
        """
        return self.__suit


CardLike = Union[str, Card]


def parse_card(card: CardLike) -> Card:
    """Parses the card-like object.

    :param card: the card-like object.
    :return: the parsed card
    """
    if isinstance(card, str) and len(card) == 2:
        return Card(Rank(card[0]), Suit(card[1]))
    elif isinstance(card, Card):
        return card
    else:
        raise TypeError('Invalid card type')
