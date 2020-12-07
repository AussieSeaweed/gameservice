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
    def _player_public_info(cls, player):
        return {
            'payoff': player.payoff,
            'actions': [str(action) for action in player.actions if action.public],
        }

    @classmethod
    def _player_private_info(cls, player):
        return {
            **cls._player_public_info(player),
            'actions': [str(action) for action in player.actions],
        }

    @classmethod
    def player_public_info(cls, player):
        return cls._player_public_info(player)

    @classmethod
    def player_private_info(cls, player):
        return cls._player_private_info(player)

    def player_info(self, player):
        return self.player_private_info(player) if player is self.player else self.player_public_info(player)

    @classmethod
    def nature_public_info(cls, nature):
        return cls._player_public_info(nature)

    @classmethod
    def nature_private_info(cls, nature):
        return cls._player_private_info(nature)

    def nature_info(self, nature):
        return self.nature_private_info(nature) if self.player.nature else self.nature_public_info(nature)

    def serialize(self):
        return {
            'environment': self.environment_info(self.game),
            'players': [self.player_info(player) for player in self.game.players],
            'nature': None if self.game.nature is None else self.nature_info(self.game.nature),
            'logs': [str(log) for log in self.game.logs],
            'terminal': self.game.terminal,
        }

    def __str__(self):
        return str(self.serialize())


class SeqInfoSet(InfoSet):
    @classmethod
    def _player_public_info(cls, player):
        return {
            **super()._player_public_info(player),
            'active': player is player.game.player,
        }
