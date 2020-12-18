from ..game import SeqInfoSet


class TTTInfoSet(SeqInfoSet):
    @classmethod
    def environment_info(cls, game):
        return {
            **super().environment_info(game),
            'board': game.board,
        }
