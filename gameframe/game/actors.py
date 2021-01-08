from abc import ABC, abstractmethod
from typing import final


class Actor(ABC):
    """Actor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold
    private information regarding a game state that no other player knows about.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    def __init__(self, game):
        self._game = game

    def __next__(self):
        if self.nature:
            return self
        else:
            return self._game.players[(self._game.players.index(self) + 1) % len(self._game.players)]

    def __str__(self):
        return 'Nature' if self.nature else f'Player {self._game.players.index(self)}'

    @property
    @final
    def information_set(self):
        """
        :return: the information set of this actor
        """
        return {
            'game': self._game._information,
            'environment': self._game.environment._information,
            'nature': self._private_information if self.nature else self._game.nature._public_information,
            'players': list(map(
                lambda player: self._private_information if self is player else player._public_information,
                self._game.players,
            )),
        }

    @property
    @final
    def nature(self):
        """
        :return: True if this actor is nature, False otherwise
        """
        return self is self._game.nature

    @property
    @abstractmethod
    def actions(self):
        """
        :return: the actions of this actor
        """
        pass

    @property
    @abstractmethod
    def payoff(self):
        """
        :return: the payoff of this actor
        """
        pass

    @property
    def _private_information(self):
        return {
            **self._public_information,
            'actions': self.actions,
        }

    @property
    def _public_information(self):
        return {
            'actions': list(filter(lambda action: action.public, self.actions)),
        }
