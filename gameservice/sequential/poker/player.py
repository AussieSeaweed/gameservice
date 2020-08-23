from typing import Dict, List, Any

from gameservice.util.poker import evaluate52
from ..game import Player


class PokerPlayer(Player):
    starting_stack: int = 200

    class Card:
        def __init__(self, card_str: str, exposed: bool):
            self.card_str: str = card_str
            self.exposed: bool = exposed

    def __init__(self, index: int):
        super().__init__(index)

        self.cards: List[PokerPlayer.Card] = []
        self.stack: int = self.starting_stack
        self.bet: int = 0

    def info(self, show_private: bool) -> Dict[str, Any]:
        info: Dict[str, Any] = super().info(show_private)

        info.update({
            "cards": [card.card_str if card.exposed or show_private else None for card in self.cards],
            "stack": self.stack,
            "bet": self.bet
        })

        return info

    """Poker player methods"""

    @property
    def total(self) -> int:
        return self.stack + self.bet

    @property
    def card_str_list(self) -> List[str]:
        return [card.card_str for card in self.cards]

    def hand(self, board_card_str_list: List[str]) -> int:
        return evaluate52(self.card_str_list + board_card_str_list)
