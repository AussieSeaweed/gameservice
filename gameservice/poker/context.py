from ..game.context import Context


class PokerContext(Context):
    def __init__(self, game):
        super().__init__(game)

        self.pot = 0
        self.board = []
        self.street = 0

        self.aggressor = None

    @property
    def info(self):
        return {
            **super().info,
            "pot": self.pot,
            "board": self.board,
            "street": self.street,
        }

    @property
    def min_raise(self):
        sorted_bets = sorted(self.game.players.bets)

        return sorted_bets[-1] + max(sorted_bets[-1] - sorted_bets[-2], max(self.game.blinds))
