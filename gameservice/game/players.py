from ..exceptions import PlayerNotFoundException


class Players:
    def __init__(self, game):
        self.game = game

        self.nature = self.game.nature_type(game)
        self.__players = [self.game.player_type(game, i) for i in range(self.game.num_players)]

    def next(self, player):
        return self[(player.index + 1) % len(self)]

    def prev(self, player):
        return self[(player.index - 1) % len(self)]

    def __len__(self):
        return len(self.__players)

    def __getitem__(self, item):
        try:
            return self.nature if item is None else self.__players[item]
        except IndexError:
            raise PlayerNotFoundException

    def __iter__(self):
        return iter(self.__players)
