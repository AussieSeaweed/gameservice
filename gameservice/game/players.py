class Players:
    def __init__(self, game):
        self.__game = game
        self.__players = tuple(game.player_type(game, i) for i in range(game.num_players))
        self.__nature = game.nature_type(game)

    @property
    def game(self):
        return self.__game

    @property
    def nature(self):
        return self.__nature

    def __len__(self):
        return len(self.__players)

    def __getitem__(self, item):
        return self.__players[item]

    def __iter__(self):
        return iter(self.__players)
