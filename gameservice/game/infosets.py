"""
This module defines info-sets in gameservice.
"""
from abc import ABC


class InfoSet(ABC):
    """
    This is a class that represents info-sets.
    """

    def __init__(self, player):
        """
        Constructs the InfoSet instance. Stores the player of the info-set.
        :param player: the player of the info-set
        """
        self.__player = player

    @property
    def player(self):
        """
        :return: the player of the info-set
        """
        return self.__player

    @property
    def game(self):
        """
        :return: the game of the info-set
        """
        return self.player.game

    @staticmethod
    def environment_info(environment):
        """
        Serializes the environment.
        :param environment: the environment of the info-set
        :return: the dictionary representation of the environment information
        """
        return {}

    @classmethod
    def _player_public_info(cls, player):
        """
        :param player: the player of the info-set
        :return: the dictionary representation of the public player information
        """
        return {
            'payoff': player.payoff,
            'actions': [str(action) for action in player.actions if action.public],
        }

    @classmethod
    def _player_private_info(cls, player):
        """
        :param player: the player of the info-set
        :return: the dictionary representation of the private player information
        """
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
        """
        Serializes the player.
        :param player: the player of the info-set
        :return: the dictionary representation of the player information
        """
        return self.player_private_info(player) if player is self.player else self.player_public_info(player)

    @classmethod
    def nature_public_info(cls, nature):
        return cls._player_public_info(nature)

    @classmethod
    def nature_private_info(cls, nature):
        return cls._player_private_info(nature)

    def nature_info(self, nature):
        """
        Serializes the nature.
        :param nature: the nature of the info-set
        :return: the dictionary representation of the nature information
        """
        return self.nature_private_info(nature) if self.player.nature else self.nature_public_info(nature)

    def serialize(self):
        """
        Serializes the game.
        :return: the dictionary representation of the game information
        """
        return {
            'environment': self.environment_info(self.game.environment),
            'players': [self.player_info(player) for player in self.game.players],
            'nature': None if self.game.nature is None else self.nature_info(self.game.nature),
            'logs': [str(log) for log in self.game.logs],
            'terminal': self.game.terminal,
        }

    def __str__(self):
        """
        Converts the info-set into a string representation.
        :return: the string representation of the info-set
        """
        return str(self.serialize())


class SeqInfoSet(InfoSet):
    """
    This is a class that represents sequential info-sets.
    """

    @classmethod
    def _player_public_info(cls, player):
        """
        :param player: the player of the sequential info-set
        :return: the dictionary representation of the public player information
        """
        return {
            **super()._player_public_info(player),
            'active': player is player.game.player,
        }
