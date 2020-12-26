"""
This module defines info-sets and sequential info-sets in gameframe.
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

    @property
    def environment_info(self):
        """
        Serializes the environment.

        :return: the dictionary representation of the environment information
        """
        return None if self.game.environment is None else {}

    @property
    def nature_public_info(self):
        """
        Serializes the nature publicly.

        :return: the dictionary representation of the public nature information
        """
        return {
            'nature': self.game.nature.nature,
            'index': self.game.nature.index,
            'payoff': self.game.nature.payoff,
            'actions': [str(action) for action in self.game.nature.actions if action.public],
            'next': str(next(self.game.nature)),
            'str': str(self.game.nature),
        }

    @property
    def nature_private_info(self):
        """
        Serializes the nature privately.

        :return: the dictionary representation of the private nature information
        """
        return {
            **self.nature_public_info,
            'actions': [str(action) for action in self.game.nature.actions],
        }

    @property
    def nature_info(self):
        """
        Serializes the nature.

        :return: the dictionary representation of the nature information
        """
        if self.game.nature is None:
            return None
        else:
            return self.nature_private_info if self.player.nature else self.nature_public_info

    def player_public_info(self, index):
        """
        Serializes the player publicly.

        :param index: the index of the player
        :return: the dictionary representation of the public player information
        """
        return {
            'nature': self.game.players[index].nature,
            'index': self.game.players[index].index,
            'payoff': self.game.players[index].payoff,
            'actions': [str(action) for action in self.game.players[index].actions if action.public],
            'next': str(next(self.game.players[index])),
            'str': str(self.game.players[index]),
        }

    def player_private_info(self, index):
        """
        Serializes the player privately.

        :param index: the index of the player
        :return: the dictionary representation of the private player information
        """
        return {
            **self.player_public_info(index),
            'actions': list(map(str, self.game.players[index].actions)),
        }

    def player_info(self, index):
        """
        Serializes the player.

        :param index: the index of the player
        :return: the dictionary representation of the player information
        """
        return self.player_private_info(index) if index == self.player.index else self.player_public_info(index)

    def serialize(self):
        """
        Serializes the game.

        :return: the dictionary representation of the game information
        """
        return {
            'environment': self.environment_info,
            'nature': self.nature_info,
            'players': list(map(self.player_info, range(len(self.game.players)))),
            'logs': list(map(str, self.game.logs)),
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
            'player': None if self.game.terminal else str(self.game.player),
        }