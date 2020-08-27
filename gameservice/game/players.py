class Players:
    def __init__(self, game):
        self.game = game
        self.__players = tuple(self._create_player(i) for i in range(game.num_players))
        self.nature = self._create_nature()

    def _create_player(self, index):
        return self.game.player_type(self.game)

    def _create_nature(self):
        return self.game.nature_type(self.game)

    def index(self, player):
        return self.__players.index(player) if player in self.__players else None

    def __len__(self):
        return len(self.__players)

    def __getitem__(self, item):
        return self.__players[item]

    def __iter__(self):
        return iter(self.__players)
