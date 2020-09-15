from gameservice.game.players import Players


class PokerPlayers(Players):
    def __init__(self, game):
        super().__init__(game)

        if game.ante is not None:
            for player in self:
                ante = min(game.ante, player.stack)

                player.stack -= ante
                player.bet += ante

        if game.blinds is not None:
            for player, blind in zip(reversed(self) if len(self) == 2 else self, game.blinds):
                blind = min(blind, player.stack)

                player.stack -= blind
                player.bet += blind

    @property
    def bets(self):
        return [player.bet for player in self]

    def next_relevant(self, player):
        if not self.num_relevant:
            return self.nature

        player = self.next(player)

        while not player.relevant and player is not self.game.context.aggressor:
            player = self.next(player)

        return self.nature if player is self.game.context.aggressor else player

    @property
    def num_relevant(self):
        return [player.relevant for player in self].count(True)

    @property
    def num_mucked(self):
        return [player.mucked for player in self].count(True)
