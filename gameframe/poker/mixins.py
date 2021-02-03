from abc import ABC, abstractmethod


class Openable(ABC):
    @abstractmethod
    def open(self) -> None:
        pass


class Closeable(ABC):
    @abstractmethod
    def close(self) -> None:
        pass
