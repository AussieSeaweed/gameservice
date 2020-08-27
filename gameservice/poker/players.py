from gameservice.game.players import Players


class PokerPlayers(Players):
    @property
    def bets(self):
        return [player.bet for player in self]

    def clear_bets(self):
        for player in self:
            player.bet = 0
