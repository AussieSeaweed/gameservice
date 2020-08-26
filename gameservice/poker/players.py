from ..game.players import Players


class PokerPlayers(Players):
    @property
    def bets(self):
        return [player.bet for player in self]

    @property
    def num_in_hand(self):
        num_in_hand = 0

        for player in self:
            num_in_hand += not player.mucked

        return num_in_hand
