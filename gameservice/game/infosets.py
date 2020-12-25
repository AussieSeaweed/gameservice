"""
This module defines info-sets and sequential info-sets in gameservice.
"""
from abc import ABC


class InfoSet(ABC):
    """
    This is a class that represents info-sets.

    The subclasses of this class should overload environment_info, nature_public_info, nature_private_info,
    player_public_info, and player_private_info methods accordingly to represent various elements of the info-set of the
    corresponding player.
    """

    def __init__(self, player):
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

    @staticmethod
    def nature_public_info(nature):
        """
        Serializes the nature publicly.

        :param nature: the nature of the info-set
        :return: the dictionary representation of the public nature information
        """
        return {
            'nature': nature.nature,
            'index': nature.index,
            'payoff': nature.payoff,
            'actions': [str(action) for action in nature.actions if action.public],
        }

    @classmethod
    def nature_private_info(cls, nature):
        """
        Serializes the nature privately.

        :param nature: the nature of the info-set
        :return: the dictionary representation of the private nature information
        """
        return {
            **cls.nature_public_info(nature),
            'actions': [str(action) for action in nature.actions],
        }

    def nature_info(self, nature):
        """
        Serializes the nature.

        :param nature: the nature of the info-set
        :return: the dictionary representation of the nature information
        """
        return self.nature_private_info(nature) if self.player.nature else self.nature_public_info(nature)

    @staticmethod
    def player_public_info(player):
        """
        Serializes the player publicly.

        :param player: the player of the info-set
        :return: the dictionary representation of the public player information
        """
        return {
            'nature': player.nature,
            'index': player.index,
            'payoff': player.payoff,
            'actions': [str(action) for action in player.actions if action.public],
        }

    @classmethod
    def player_private_info(cls, player):
        """
        Serializes the player privately.

        :param player: the player of the info-set
        :return: the dictionary representation of the private player information
        """
        return {
            **cls.player_public_info(player),
            'actions': [str(action) for action in player.actions],
        }

    def player_info(self, player):
        """
        Serializes the player.

        :param player: the player of the info-set
        :return: the dictionary representation of the player information
        """
        return self.player_private_info(player) if player is self.player else self.player_public_info(player)

    def serialize(self):
        """
        Serializes the game.

        :return: the dictionary representation of the game information
        """
        return {
            'environment': self.environment_info(self.game.environment),
            'nature': None if self.game.nature is None else self.nature_info(self.game.nature),
            'players': [self.player_info(player) for player in self.game.players],
            'logs': [str(log) for log in self.game.logs],
            'terminal': self.game.terminal,
        }

    def __str__(self):
        return str(self.serialize())


class SequentialInfoSet(InfoSet):
    """
    This is a class that represents sequential info-sets.
    """

    def serialize(self):
        return {
            **super().serialize(),
            'player': str(self.game.player),
        }
