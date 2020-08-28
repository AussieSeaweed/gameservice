from ..game.players import Players


class TicTacToePlayers(Players):
    def _create_players(self):
        return [self.game.player_type(self.game), self.game.player_type(self.game)]
