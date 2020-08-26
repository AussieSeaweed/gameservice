from ..game.players import Players


class PokerPlayers(Players):
    @property
    def bets(self):
        return [player.bet for player in self]
