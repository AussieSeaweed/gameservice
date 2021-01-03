from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Iterator, Optional, Sequence, TypeVar, Union, final

from gameframe.game.exceptions import PlayerTypeMismatchException, TerminalityException
from gameframe.utils import override

G = TypeVar('G', bound='Game')
E = TypeVar('E', bound='Environment')
N = TypeVar('N', bound='Actor')
P = TypeVar('P', bound='Actor')


class Game(Generic[G, E, N, P], ABC):
    """Game is the abstract base class for all games.

    It provides a rigid definition on which various games can be defined. Every game has the following entities that
    need to be defined:

        - The game
        - The environment
        - The nature
        - The players

    The game class is a wrapper class that envelops all the elements of the game: the environment, the nature, and
    the players. They each represent entities of the game.

    The environment contains global information about a game state that does not belong to any actor in particular and
    is public.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold
    private information regarding a game state that no other player knows about. However, the nature should not be
    aware of any private information held by other players in the game.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    def __init__(self, environment: E, nature: N, players: Sequence[P]) -> None:
        self.__environment: E = environment
        self.__nature: N = nature
        self.__players: Sequence[P] = players

    @property
    @final
    def environment(self) -> E:
        """
        :return: the environment of the game
        """
        return self.__environment

    @property
    @final
    def nature(self) -> N:
        """
        :return: the nature of the game
        """
        return self.__nature

    @property
    @final
    def players(self) -> Sequence[P]:
        """
        :return: the players of the game
        """
        return self.__players

    @property
    @abstractmethod
    def terminal(self) -> bool:
        """
        :return: True if the game is terminal, False otherwise
        """
        pass

    @property
    def _information(self) -> Dict[str, Any]:
        return {}


class Environment(Generic[G, E, N, P]):
    """Environment is the base class for all environments."""

    def __init__(self, game: G) -> None:
        self.__game: G = game

    @property
    @final
    def game(self) -> G:
        """
        :return: the game of the environment
        """
        return self.__game

    @property
    def _information(self) -> Dict[str, Any]:
        return {}


class Actor(Generic[G, E, N, P], Iterator[Union[N, P]], ABC):
    """Actor is the abstract base class for all actors."""

    def __init__(self, game: G) -> None:
        self.__game: G = game

    @property
    @final
    def game(self) -> G:
        """
        :return: the game of the actor
        """
        return self.__game

    @property
    @final
    def nature(self) -> bool:
        """
        :return: True if the actor is nature, False otherwise
        """
        return self is self.game.nature

    @property
    @final
    def index(self) -> Optional[int]:
        """
        :return: the index of the actor
        """
        return None if self.nature else self.game.players.index(self)

    @property
    @final
    def information_set(self) -> Dict[str, Any]:
        """
        :return: the information set of the actor
        """
        return {
            'game': self.game._information,
            'environment': self.game.environment._information,
            'nature': self.game.nature._private_information if self.nature else self.game.nature._public_information,
            'players': list(map(
                lambda player: player._private_information if self is player else player._public_information,
                self.game.players,
            )),
        }

    @property
    @abstractmethod
    def actions(self) -> Sequence[Action[G, E, N, P]]:
        """
        :return: the actions of the actor
        """
        pass

    @property
    @abstractmethod
    def payoff(self) -> int:
        """
        :return: the payoff of the actor
        """
        pass

    @override
    def __next__(self) -> Union[N, P]:
        return self if self.index is None else self.game.players[(self.index + 1) % len(self.game.players)]

    @override
    def __str__(self) -> str:
        return 'Nature' if self.nature else f'Player {self.index}'

    @property
    def _private_information(self) -> Dict[str, Any]:
        return {
            **self._public_information,
            'actions': self.actions,
        }

    @property
    def _public_information(self) -> Dict[str, Any]:
        return {
            'actions': list(filter(lambda action: action.public, self.actions)),
        }


class Action(Generic[G, E, N, P], ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, actor: Union[N, P], chance: bool, public: bool) -> None:
        self.__actor: Union[N, P] = actor

        self.__chance: bool = chance
        self.__public: bool = public

    @property
    @final
    def actor(self) -> Union[N, P]:
        """
        :return: the actor of the action
        """
        return self.__actor

    @property
    @final
    def game(self) -> G:
        """
        :return: the game of the action
        """
        return self.actor.game

    @property
    @final
    def chance(self) -> bool:
        """
        :return: True if the action is a chance action, False otherwise
        """
        return self.__chance

    @property
    @final
    def public(self) -> bool:
        """
        :return: True if the action is a public action, False otherwise
        """
        return self.__public

    def act(self) -> None:
        """Applies the action to the game of the action.

        The overridden act method should first call the super method and then make the necessary modifications to the
        game.

        :return: None
        :raise GameFrameException: if the action integrity verification fails prior to the action
        """
        self._verify()

    @abstractmethod
    @override
    def __str__(self) -> str:
        pass

    def _verify(self) -> None:
        if self.game.terminal:
            raise TerminalityException()
        elif self.chance != self.actor.nature:
            raise PlayerTypeMismatchException()
