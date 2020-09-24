from ..poker.actions import Deal


class NLHEPreFlop(Deal):
    def __init__(self, game, player):
        super().__init__(game, player, 2)

    @property
    def opener(self):
        return self.game.players[1 if self.game.num_players == 2 else 2]
