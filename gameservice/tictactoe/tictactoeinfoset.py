from ..game import SequentialInfoSet


class TicTacToeInfoSet(SequentialInfoSet):
    @classmethod
    def environment_info(cls, game):
        return {
            **super().environment_info(game),
            "board": game.board
        }
