from ..game import SequentialInfoSet


class PokerInfoSet(SequentialInfoSet):
    @classmethod
    def environment_info(cls, game):
        return {
            **super().environment_info(game),
            'pot': game.pot,
            'board': game.board,
        }

    @classmethod
    def player_public_info(cls, player):
        return {
            **super().player_public_info(player),
            'stack': player.stack,
            'bet': player.bet,
            'hole_cards': None if player.hole_cards is None else [card if player.game.terminal else None for card in
                                                                  player.hole_cards],
        }

    @classmethod
    def player_private_info(cls, player):
        return {
            **super().player_private_info(player),
            'hole_cards': player.hole_cards,
        }
