from __future__ import annotations

from enum import Enum


class Rank(Enum):
    """Rank is the enum for ranks."""
    TWO: str = '2'
    THREE: str = '3'
    FOUR: str = '4'
    FIVE: str = '5'
    SIX: str = '6'
    SEVEN: str = '7'
    EIGHT: str = '8'
    NINE: str = '9'
    TEN: str = 'T'
    JACK: str = 'J'
    QUEEN: str = 'Q'
    KING: str = 'K'
    ACE: str = 'A'


class Suit(Enum):
    """Suit is the enum for suits."""
    CLUB: str = 'c'
    DIAMOND: str = 'd'
    HEART: str = 'h'
    SPADE: str = 's'


class Card:
    """Card is the base class for all cards."""

    def __init__(self: Card, rank: Rank, suit: Suit) -> None:
        self.__rank: Rank = rank
        self.__suit: Suit = suit

    def __str__(self: Card) -> str:
        return self.__rank.value + self.__suit.value


class HoleCard(Card):
    """HoleCard is the class for hole cards."""

    def __init__(self, rank: Rank, suit: Suit, status: bool) -> None:
        super().__init__(rank, suit)

        self.__status: bool = status

    @property
    def status(self: HoleCard) -> bool:
        return self.__status
