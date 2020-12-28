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


class Suit(Enum):
    """Suit is the enum for suits."""
    CLUB = 'c'
    DIAMOND = 'd'
    HEART = 'h'
    SPADE = 's'


class Card:
    """Card is the class for cards."""

    def __init__(self, rank: Rank, suit: Suit):
        self.__rank: Rank = rank
        self.__suit: Suit = suit

    def __str__(self) -> str:
        return self.__rank.value + self.__suit.value
