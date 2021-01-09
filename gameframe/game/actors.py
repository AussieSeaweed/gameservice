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
        return self if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        return 'Nature' if self.nature else f'Player {self.index}'

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
        return self.game.players.index(self)

    @property
    def information_set(self):
        """
        :return: the information set of this actor
        """
        return {
            'game': self.game.information,
            'environment': self.game.environment.information,
            'nature': self.private_information if self.nature else self.game.nature.public_information,
            'players': list(map(
                lambda player: self.private_information if self is player else player.public_information,
                self.game.players,
            )),
        }

    @property
    def nature(self):
        """
        :return: True if this actor is nature, False otherwise
        """
        return self is self.game.nature

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
    def private_information(self):
        """
        :return: the private information of this actor
        """
        return {
            **self.public_information,
            'actions': self.actions,
        }

    @property
    def public_information(self):
        """
        :return: the public information of this actor
        """
        return {
            'actions': list(filter(lambda action: action.public, self.actions)),
        }
