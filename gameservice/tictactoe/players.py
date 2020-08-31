from ..game.players import Players


class TicTacToePlayers(Players):
    def _create_players(self):
        players = [self.game.player_type(self.game), self.game.player_type(self.game)]

        for player in players:
            player.payoff = -1

        return players
