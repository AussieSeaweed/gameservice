from abc import ABC, abstractmethod
from typing import Optional

from gameframe.game import BaseActor, BaseEnv


class BaseSeqEnv(BaseEnv, ABC):
    """BaseSeqEnv is the abstract base class for all sequential environments."""

    @property
    @abstractmethod
    def actor(self) -> Optional[BaseActor]:
        """
        :return: the actor of the sequential game of this environment
        """
        pass
