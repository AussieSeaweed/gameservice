from gameservice.game.players import Players


class PokerPlayers(Players):
    def _create_players(self):
        return [self.game.player_type(self.game, i) for i in range(self.game.num_players)]

    @property
    def bets(self):
        return [player.bet for player in self]

    def next_relevant(self, player):
        if not self.num_relevant:
            return self.nature

        player = self.next(player)

        while not player.relevant:
            player = self.next(player)

        return player

    @property
    def num_relevant(self):
        return [player.relevant for player in self].count(True)

    @property
    def num_mucked(self):
        return [player.mucked for player in self].count(True)
