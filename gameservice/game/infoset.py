"""
This module defines a general game info-set in gameservice.
"""
from abc import ABC


class InfoSet(ABC):
    """
    This is a base class for all info-sets of games in gameservice.
    """

    def __init__(self, player):
        """
        Constructs the InfoSet instance.
        :param player: the player on which the information set is constructed
        """
        self.__player = player

    @property
    def player(self):
        """
        Returns the player of the info-set.
        :return: the player of the info-set
        """
        return self.__player

    @property
    def game(self):
        """
        Returns the game of the info-set.
        :return: the game of the info-set
        """
        return self.player.game

    @staticmethod
    def environment_info(environment):
        """
        Returns the dictionary representation of the information of the environment.
        :param environment: the environment to be analyzed
        :return: the dictionary representation of the information of the environment
        """
        return {}

    @classmethod
    def _player_public_info(cls, player):
        """
        Returns the dictionary representation of the public information of the player.
        :param player: the player to be analyzed
        :return: the dictionary representation of the public information of the player
        """
        return {
            'payoff': player.payoff,
            'actions': [str(action) for action in player.actions if action.public],
        }

    @classmethod
    def _player_private_info(cls, player):
        """
        Returns the dictionary representation of the private information of the player.
        :param player: the player to be analyzed
        :return: the dictionary representation of the private information of the player
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
        Returns the dictionary representation of the information of the player.
        :param player: the player to be analyzed
        :return: the dictionary representation of the information of the player
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
        Returns the dictionary representation of the information of the nature.
        :param nature: the nature to be analyzed
        :return: the dictionary representation of the information of the nature
        """
        return self.nature_private_info(nature) if self.player.nature else self.nature_public_info(nature)

    def serialize(self):
        """
        Returns the dictionary representation of the game.
        :return: the dictionary representation of the game
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
        Returns the string representation of the info-set.
        :return: the string representation of the info-set
        """
        return str(self.serialize())


class SeqInfoSet(InfoSet):
    """
    This is a base class for all info-sets of sequential games in gameservice.
    """

    @classmethod
    def _player_public_info(cls, player):
        """
        Returns the dictionary representation of the public information of the player in a sequential game.
        :param player: the player to be analyzed
        :return: the dictionary representation of the public information of the player in a sequential game.
        """
        return {
            **super()._player_public_info(player),
            'active': player is player.game.player,
        }
