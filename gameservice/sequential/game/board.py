from abc import abstractmethod, ABC
from typing import Dict, Any


class Board(ABC):
    @property
    @abstractmethod
    def info(self) -> Dict[str, Any]:
        pass
