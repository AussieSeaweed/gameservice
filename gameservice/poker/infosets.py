"""
This module defines poker info-sets in gameservice.
"""
from ..game import SequentialInfoSet


class PokerInfoSet(SequentialInfoSet):
    """
    This is a class that represents poker info-sets.
    """

    @classmethod
    def environment_info(cls, environment):
        return {
            **super().environment_info(environment),
            'min_delta': environment.min_delta,
            'pot': environment.pot,
            'board': list(map(str, environment.board)),
        }

    @classmethod
    def player_public_info(cls, player):
        return {
            **super().player_public_info(player),
            'stack': player.stack,
            'bet': player.bet,
            'hole_cards': None if player.hole_cards is None else [str(card) if player.game.terminal else None for card
                                                                  in player.hole_cards],
            'aggressive': player is player.game.environment.aggressor,
        }

    @classmethod
    def player_private_info(cls, player):
        return {
            **super().player_private_info(player),
            'hole_cards': None if player.hole_cards is None else list(map(str, player.hole_cards)),
        }
