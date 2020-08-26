from ..game.context import Context


class PokerContext(Context):
    def __init__(self, game):
        super().__init__(game)

        self.pot = 0
        self.board = []

    @property
    def info(self):
        return {
            **super().info,
            "pot": self.pot,
            "board": self.board,
        }
