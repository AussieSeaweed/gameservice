from ..game import InfoSet


class SequentialInfoSet(InfoSet):
    """
    This is a class that represents sequential info-sets.
    """

    def serialize(self):
        return {
            **super().serialize(),
            'player': None if self.game.terminal else str(self.game.player),
        }
