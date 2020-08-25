from ..exceptions import InvalidActionArgumentException
from ..sequential.action import SequentialAction


class Mark(SequentialAction):
    def __init__(self, game, player, r, c):
        super().__init__(game, player)

        if [r, c] not in game.context.empty_coords:
            raise InvalidActionArgumentException

        self.r = r
        self.c = c

    @property
    def label(self):
        return f"Mark {self.r} {self.c}"

    def act(self):
        self.game.context.board[self.r][self.c] = self.player.index
        self.game.update()
