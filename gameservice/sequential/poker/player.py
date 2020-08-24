from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..game.player import Player


class PokerPlayer(Player, ABC):
    class Card:
        def __init__(self, card_str: str, private: bool):
            self.str: str = card_str
            self.private: bool = private

    def __init__(self, index: int, starting_stack: int):
        super().__init__(index)

        self.cards: List[PokerPlayer.Card] = []
        self.stack: int = starting_stack
        self.bet: int = 0

    def get_info(self, show_private: bool) -> Dict[str, Any]:
        return {
            **super().get_info(show_private),

            "cards": [card.str if not card.private or show_private else None for card in self.cards],
            "stack": self.stack,
            "bet": self.bet,
        }

    def get_card_str_list(self) -> List[str]:
        return list(map(lambda card: card.card_str, self.cards))

    @abstractmethod
    def get_hand_rank(self, board: List[str]) -> int:
        """
        the Lower the rank the better the hand

        :param board: string card values of the board
        :return: hand rank when combined with the player's hole cards
        """
