from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, game, index):
        self.__game = game
        self.__index = index

    @property
    def game(self):
        return self.__game

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
        }

    @property
    @abstractmethod
    def actions(self):
        pass


class Nature(Player, ABC):
    @property
    def nature(self):
        return True
