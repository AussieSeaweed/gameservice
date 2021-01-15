from abc import ABC, abstractmethod


class Actor(ABC):
    """Actor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold
    private information regarding a game state that no other player knows about.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    def __init__(self, game):
        self.__game = game

    def __next__(self):
        return self if self.is_nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        return 'Nature' if self.is_nature else f'Player {self.index}'

    @property
    def game(self):
        """
        :return: the game of this actor
        """
        return self.__game

    @property
    def index(self):
        """
        :return: the index of this actor
        """
        return None if self.is_nature else self.game.players.index(self)

    @property
    def information_set(self):
        """
        :return: the information set of this actor
        """
        return {
            'game': self.game._information,
            'environment': self.game.environment._information,
            'nature': self._private_information if self.is_nature else self.game.nature._public_information,
            'players': tuple(map(
                lambda player: self._private_information if self is player else player._public_information,
                self.game.players,
            )),
        }

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
    def is_nature(self):
        """
        :return: True if this actor is nature, else False
        """
        return self is self.game.nature

    @property
    def _private_information(self):
        return {
            **self._public_information,
            'actions': tuple(self.actions),
        }

    @property
    def _public_information(self):
        return {
            'actions': tuple(filter(lambda action: action.is_public, self.actions)),
        }
