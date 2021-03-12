from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Optional, TypeVar, Union, final

from gameframe.exceptions import ActionException
from gameframe.game import Game, _A, _Action, _N, _P


class SequentialGame(Game[_N, _P], ABC):
    """SequentialGame is the abstract generic base class for all sequential games.

       In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game
       is terminal, its actor attribute must be set to None to denote such.
    """

    def __init__(self, nature: _N, players: Iterable[_P], actor: Optional[Union[_N, _P]]):
        super().__init__(nature, players)

        self._actor = actor

    @property
    @final
    def terminal(self) -> bool:
        return self._actor is None

    @property
    @final
    def actor(self) -> Optional[Union[_N, _P]]:
        """
        :return: The actor of this sequential game.
        """
        return self._actor


_SG = TypeVar('_SG', bound=SequentialGame[Any, Any])


class _SequentialAction(_Action[_SG, _A], ABC):
    @property
    @abstractmethod
    def next_actor(self) -> Any:
        pass

    def act(self) -> None:
        super().act()

        self.game._actor = self.next_actor

    def verify(self) -> None:
        super().verify()

        if self.game._actor is not self.actor:
            raise ActionException('The actor is not in turn')
