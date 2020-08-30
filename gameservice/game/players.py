from ..exceptions import PlayerNotFoundException


class Players:
    def __init__(self, game):
        self.game = game
        self.__players = self._create_players()
        self.nature = self._create_nature()

    def _create_players(self):
        return []

    def _create_nature(self):
        return self.game.nature_type(self.game)

    def index(self, player):
        try:
            return None if player is self.nature else self.__players.index(player)
        except ValueError:
            raise PlayerNotFoundException

    def next(self, player):
        return self[(self.index(player) + 1) % len(self)]

    def prev(self, player):
        return self[(self.index(player) - 1) % len(self)]

    def __len__(self):
        return len(self.__players)

    def __getitem__(self, item):
        try:
            return self.__players[item]
        except IndexError:
            raise PlayerNotFoundException

    def __iter__(self):
        return iter(self.__players)
