from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Optional, TypeVar, Union, final

from gameframe.exceptions import GameFrameError
from gameframe.game import BaseActor, BaseGame, Game, _A, _Action, _N, _P


class BaseSequentialGame(BaseGame, ABC):
    """BaseSequentialGame is the base abstract class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    @property
    @abstractmethod
    def actor(self) -> Optional[BaseActor]:
        """Returns the current actor of this sequential game.

        :return: The current actor of this sequential game.
        """
        ...

    @property
    @final
    def terminal(self) -> bool:
        return self.actor is None


_G = TypeVar('_G', bound=BaseSequentialGame)


class SequentialGame(Game[_N, _P], BaseSequentialGame, ABC):
    """SequentialGame is the abstract class for all sequential games.

    :param initial_actor_index: The initial actor index. If it is None, the initial actor is set to the nature.
    :param nature: The nature of this game.
    :param players: The players of this game.
    """

    def __init__(self, initial_actor_index: Optional[int], nature: _N, players: Iterable[_P]):
        super().__init__(nature, players)

        self._actor: Optional[Union[_N, _P]]

        if initial_actor_index is None:
            self._actor = self.nature
        else:
            self._actor = self.players[initial_actor_index]

    @property
    @final
    def actor(self) -> Optional[Union[_N, _P]]:
        return self._actor


class _SequentialAction(_Action[_G, _A]):
    def verify(self) -> None:
        super().verify()

        if self.game.actor is not self.actor:
            raise GameFrameError('The actor is not in turn')
