from .utils import nested_str


class InfoSet:
    def __init__(self, player):
        self.__player = player

    @property
    def player(self):
        return self.__player

    @property
    def game(self):
        return self.player.game

    @staticmethod
    def environment_info(game):
        return {}

    @classmethod
    def player_public_info(cls, player):
        return {
            "index": player.index,
            "nature": player.nature,
            "payoff": player.payoff,
            "actions": [str(action) for action in player.actions if action.public]
        }

    @classmethod
    def player_private_info(cls, player):
        return {
            **cls.player_public_info(player),
            "actions": [str(action) for action in player.actions]
        }

    @classmethod
    def nature_public_info(cls, player):
        return {
            "index": player.index,
            "nature": player.nature,
            "payoff": player.payoff,
            "actions": [str(action) for action in player.actions if action.public]
        }

    @classmethod
    def nature_private_info(cls, player):
        return {
            **cls.nature_public_info(player),
            "actions": [str(action) for action in player.actions]
        }

    def player_info(self, player):
        return self.player_private_info(player) if player is self.player else self.player_public_info(player)

    def nature_info(self, nature):
        return self.nature_private_info(nature) if nature is self.player else self.nature_public_info(nature)

    def serialize(self):
        return {
            "environment": self.environment_info(self.game),
            "players": [self.player_info(player) for player in self.game.players],
            "nature": None if self.game.nature is None else self.nature_info(self.game.nature),
            "logs": [str(log) for log in self.game.logs],
            "terminal": self.game.terminal
        }

    def __str__(self):
        return nested_str(self.serialize())


class SequentialInfoSet(InfoSet):
    @classmethod
    def player_public_info(cls, player):
        return {
            **super().player_public_info(player),
            "active": player is player.game.player
        }
