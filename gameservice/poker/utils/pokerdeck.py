from abc import ABC, abstractmethod

from treys import Card, Deck

from .pokercard import PokerCard


class PokerDeck(ABC):
    @abstractmethod
    def draw(self, num_cards):
        pass

    @abstractmethod
    def peek(self, num_cards):
        pass


class PokerStdDeck(PokerDeck):
    def __init__(self):
        self.__deck = Deck()

    def draw(self, num_cards):
        card_ints = [self.__deck.draw(1)] if num_cards == 1 else self.__deck.draw(num_cards)

        return [PokerCard(Card.int_to_str(card_int)) for card_int in card_ints]

    def peek(self, num_cards):
        return [PokerCard(Card.int_to_str(card_int)) for card_int in self.__deck.cards[:num_cards]]
