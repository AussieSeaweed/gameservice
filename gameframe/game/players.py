from abc import ABC, abstractmethod


class Player(ABC):
    """Player is the abstract base class for all players."""

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """
        :return: the game of the player
        """
        return self.__game

    @property
    def index(self):
        """
        :return: the index of the player
        """
        return None if self.nature else self.game.players.index(self)

    @property
    def information_set(self):
        """
        :return: the information set of the player
        """
        return {
            'game': self.game._information,
            'environment': self.game.environment._information,
            'nature': self.game.nature._private_information if self.nature else self.game.nature._public_information,
            'players': list(map(
                lambda player: player._private_information if self is player else player._public_information,
                self.game.players)),
        }

    @property
    def nature(self):
        """
        :return: True if the player is nature, False otherwise
        """
        return self is self.game.nature

    def __next__(self):
        return self if self.index is None else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        return 'Nature' if self.nature else f'Player {self.index}'

    @property
    @abstractmethod
    def actions(self):
        """
        :return: the actions of the player
        """
        pass

    @property
    @abstractmethod
    def payoff(self):
        """
        :return: the payoff of the player
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
