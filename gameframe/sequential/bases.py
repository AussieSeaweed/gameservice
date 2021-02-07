from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from gameframe.game.bases import BaseActor, BaseGame


class BaseSeqGame(BaseGame, ABC):
    """BaseSeqGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    _actor: Optional[BaseActor]

    @property
    def terminal(self) -> bool:
        return self._actor is None

    @property
    @abstractmethod
    def actor(self) -> Optional[BaseActor]:
        """
        :return: the actor of this sequential game
        """
        pass
