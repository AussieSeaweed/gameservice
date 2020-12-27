from abc import ABC
from typing import Generic
from json import dumps

from .utils import E, G, N, P


class InfoSet(Generic[G, E, N, P], ABC):
    """InfoSet is the abstract base class for all info-sets."""

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
            'actions': list(map(str, filter(lambda action: action.public, self.game.nature.actions))),
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
            'actions': list(map(str, self.game.nature.actions)),
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
            'actions': list(map(str, filter(lambda action: action.public, self.game.players[index].actions))),
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

    def __eq__(self, other):
        return self.serialize() == other.serialize() if isinstance(other, InfoSet) else False

    def __str__(self):
        return dumps(self.serialize(), indent=4)
