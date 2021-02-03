from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from gameframe.game.bases import BaseActor, BaseEnv, BaseGame


class BaseSeqGame(BaseGame, ABC):
    """BaseSeqGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    @property
    @abstractmethod
    def env(self) -> BaseSeqEnv:
        pass

    @property
    def is_terminal(self) -> bool:
        return self.env.actor is None


class BaseSeqEnv(BaseEnv, ABC):
    """BaseSeqEnv is the abstract base class for all sequential environments."""

    _actor: Optional[BaseActor] = None

    @property
    @abstractmethod
    def actor(self) -> Optional[BaseActor]:
        """
        :return: the actor of the sequential game of this environment
        """
        pass
