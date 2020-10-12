from abc import ABC, abstractmethod
from typing import List

from treys import Deck, Card


class PokerDeck(ABC):
    @abstractmethod
    def draw(self, num_cards: int) -> List[str]:
        pass

    @abstractmethod
    def peek(self, num_cards: int) -> List[str]:
        pass


class PokerDeck52(PokerDeck):
    def __init__(self):
        self.__deck: Deck = Deck()

    def draw(self, num_cards: int) -> List[str]:
        card_ints: List[int] = [self.__deck.draw(1)] if num_cards == 1 else self.__deck.draw(num_cards)

        return [Card.int_to_str(card_int) for card_int in card_ints]

    def peek(self, num_cards: int) -> List[str]:
        return [Card.int_to_str(card_int) for card_int in self.__deck.cards[:num_cards]]
