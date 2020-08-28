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
        return self.__players.index(player) if player in self.__players else None

    def next(self, player):
        return self[(self.index(player) + 1) % len(self)]

    def prev(self, player):
        return self[(self.index(player) - 1) % len(self)]

    def __len__(self):
        return len(self.__players)

    def __getitem__(self, item):
        return self.__players[item]

    def __iter__(self):
        return iter(self.__players)
