from abc import ABC, abstractmethod
from typing import Generic, Iterable, Sequence, TypeVar

from gameframe.game.exceptions import ActionException

E = TypeVar('E', bound='Environment')
N = TypeVar('N', bound='Nature')
P = TypeVar('P', bound='Player')


class Game(Generic[E, N, P], ABC):
    """Game is the abstract base class for all games.

    Every game has the following elements that need to be defined: the
    environment, the nature, and the players.
    """

    def __init__(self, environment: E, nature: N, players: Iterable[P]):
        self.__environment: E = environment
        self.__nature: N = nature
        self.__players: Sequence[P] = tuple(players)

    @property
    def environment(self) -> E:
        """
        :return: the environment of this game
        """
        return self.__environment

    @property
    def nature(self) -> N:
        """
        :return: the nature of this game
        """
        return self.__nature

    @property
    def players(self) -> Sequence[P]:
        """
        :return: the players of this game
        """
        return self.__players

    @property
    @abstractmethod
    def is_terminal(self) -> bool:
        """
        :return: True if this game is terminal, else False
        """
        pass


class Action(ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, game: Game[E, N, P]):
        self.__game = game

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def is_applicable(self) -> bool:
        """
        :return: True if this action can be applied else False
        """
        return not self.__game.is_terminal

    def act(self) -> None:
        """Applies this action to the game.

        The overridden act method should first call the super method and then
        make the changes in the game.

        :return: None
        :raise ActionException: if this action cannot be applied
        """
        if not self.is_applicable:
            raise ActionException()


class Environment(ABC):
    """Environment is the base class for all environments.

    The environment contains global information about a game state that does
    not belong to any actor in particular and is public.
    """
    pass


class Actor(ABC):
    """Actor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.
    """

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    @abstractmethod
    def is_nature(self) -> bool:
        """
        :return: True if this actor is nature, else False
        """
        pass

    @property
    @abstractmethod
    def actions(self) -> Iterable[Action]:
        """
        :return: the actions of this actor
        """
        pass


class Nature(Actor, ABC):
    """Nature is the abstract base class for all nature actors.

    The nature is an actor that represents the environment and carries out
    chance actions. The nature may hold private information regarding a game
    state that no other player knows about.
    """

    def __str__(self) -> str:
        return 'Nature'

    @property
    def is_nature(self) -> bool:
        return True


class Player(Actor, ABC):
    """Player is the abstract base class for all players.

    The players of the game are the actors that act non-chance actions. A
    player is aware of the environment information, all the public information
    of other actors, and the private information of itself.
    """

    def __init__(self: P, game: Game[E, N, P]):
        self.__game = game

    def __next__(self) -> P:
        return self.__game.players[(self.index + 1) % len(self.__game.players)]

    def __str__(self) -> str:
        return f'Player {self.index}'

    @property
    def index(self) -> int:
        return self.__game.players.index(self)

    @property
    def is_nature(self) -> bool:
        return False
