class Player:
    def __init__(self, game, index):
        self.__game = game
        self.__index = index

    @property
    def game(self):
        return self.__game

    @property
    def index(self):
        return self.__index

    @property
    def nature(self):
        return False

    @property
    def public_info(self):
        return {
            "index": self.__index
        }

    @property
    def private_info(self):
        return self.public_info

    @property
    def infoset(self):
        return {
            "players": [player.private_info if self is player else player.public_info for player in self.game.players],
            "context": self.game.context.info,
            "action": list(self.actions),
        }

    @property
    def actions(self):
        return self.game.actions_type(self.game, self)


class Nature(Player):
    def __init__(self, game):
        super().__init__(game, None)

    @property
    def nature(self):
        return True
