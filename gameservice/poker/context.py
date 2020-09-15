from ..game.context import Context


class PokerContext(Context):
    def __init__(self, game):
        super().__init__(game)

        self.pot = 0
        self.board = []

        self.aggressor = None
        self.street = 0

    @property
    def info(self):
        return {
            **super().info,
            "pot": self.pot,
            "board": self.board,
        }

    @property
    def min_raise(self):
        sorted_bets = sorted(self.game.players.bets)

        return sorted_bets[-1] + max(sorted_bets[-1] - sorted_bets[-2], max(self.game.blinds))
