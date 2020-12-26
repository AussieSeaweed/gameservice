"""
This module defines poker info-sets in gameservice.
"""
from ..game import SequentialInfoSet


class PokerInfoSet(SequentialInfoSet):
    """
    This is a class that represents poker info-sets.
    """

    @property
    def environment_info(self):
        return {
            **super().environment_info,
            'aggressor': None if self.game.environment.aggressor is None else str(self.game.environment.aggressor),
            'min_delta': self.game.environment.min_delta,
            'pot': self.game.environment.pot,
            'board': list(map(str, self.game.environment.board)),
        }

    def player_public_info(self, index):
        return {
            **super().player_public_info(index),
            'stack': self.game.players[index].stack,
            'bet': self.game.players[index].bet,
            'hole_cards': None if self.game.players[index].hole_cards is None else [
                str(card) if self.game.terminal else None for card in self.game.players[index].hole_cards
            ],
        }

    def player_private_info(self, index):
        return {
            **super().player_private_info(index),
            'hole_cards': None if self.game.players[index].hole_cards is None else list(
                map(str, self.game.players[index].hole_cards)),
        }
