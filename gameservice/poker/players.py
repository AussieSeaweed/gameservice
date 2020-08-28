from gameservice.game.players import Players


class PokerPlayers(Players):
    def _create_players(self):
        return [self.game.player_type(self.game) for i in range(self.game.num_players)]

    @property
    def bets(self):
        return [player.bet for player in self]
