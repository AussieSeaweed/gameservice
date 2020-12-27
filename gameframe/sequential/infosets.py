from .utils import G
from ..game import E, InfoSet, N, P


class SequentialInfoSet(InfoSet[G, E, N, P]):
    """SequentialInfoSet is the abstract base class for all sequential info-sets."""

    def serialize(self):
        return {
            **super().serialize(),
            'player': None if self.game.terminal else str(self.game.player),
        }
