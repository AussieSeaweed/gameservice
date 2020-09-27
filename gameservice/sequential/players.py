from abc import ABC

from ..game.players import Player


class SequentialPlayer(Player, ABC):
    @property
    def public_info(self):
        return {
            **super().public_info,
            "active": self.game.player is self,
        }
