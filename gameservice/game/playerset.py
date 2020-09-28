from ..exceptions import PlayerNotFoundException


class PlayerSet:
    def __init__(self, game):
        self.game = game

        self.nature = self.game.nature_type(game)
        self.__players = [self.game.player_type(game, i) for i in range(self.game.num_players)]

        self.__lookup = {
            None: self.nature,
            **{player.index: player for player in self},
            **{player.label: player for player in self if player.label is not None},
        }

    def next(self, player):
        return self[(player.index + 1) % len(self)]

    def prev(self, player):
        return self[(player.index - 1) % len(self)]

    def __len__(self):
        return len(self.__players)

    def __getitem__(self, item):
        try:
            return self.__lookup[item]
        except KeyError:
            raise PlayerNotFoundException

    def __iter__(self):
        return iter(self.__players)
