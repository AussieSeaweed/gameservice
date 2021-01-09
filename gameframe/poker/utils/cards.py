from enum import Enum


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

    def __init__(self, rank, suit):
        self.__rank = rank
        self.__suit = suit

    def __str__(self):
        return self.rank.value + self.suit.value

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit


class HoleCard(Card):
    """HoleCard is the class for hole cards."""

    def __init__(self, card, status):
        super().__init__(card.rank, card.suit)

        self.status = status
