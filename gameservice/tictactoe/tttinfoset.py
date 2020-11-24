from ..game import SequentialInfoSet


class TTTInfoSet(SequentialInfoSet):
    @classmethod
    def environment_info(cls, game):
        return {
            **super().environment_info(game),
            'board': game.board,
        }
