from abc import ABC
from typing import Iterable, Union

from gameframe.game import Action, Game
from gameframe.game.bases import E, N, P


class SequentialGame(Game[E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the
    actor property. If a sequential game is terminal, its actor attribute must
    be set to None to denote such.
    """

    def __init__(self, env: E, nature: N, players: Iterable[P],
                 initial_actor: Union[N, P]):
        super().__init__(env, nature, players)

        self._actor = initial_actor

    @property
    def actor(self) -> Union[N, P]:
        """
        :return: the actor of this sequential game
        """
        return self._actor

    @property
    def is_terminal(self) -> bool:
        return self.actor is None


class SequentialAction(Action, ABC):
    """SequentialAction is the abstract base class for all sequential actions.
    """

    def __init__(self, seq_game: SequentialGame[E, N, P], actor: Union[N, P]):
        """
        TODO: rename '__seq_game' to '__game' and 'seq_game' to 'game' when...
        TODO: mypy supports private members with same names across classes.
        """
        super().__init__(seq_game)
        
        self.__seq_game = seq_game
        self.__actor = actor

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self.__actor is self.__seq_game.actor
