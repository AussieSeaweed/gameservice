from ..exceptions import ActionArgumentException
from ..sequential.actions import SequentialAction


class Mark(SequentialAction):
    def __init__(self, game, player, r, c):
        super().__init__(game, player)

        if [r, c] not in game.context.empty_coords:
            raise ActionArgumentException(f"Coordinate {r} {c} is not empty")

        self.r = r
        self.c = c

    @property
    def name(self):
        return f"Mark {self.r} {self.c}"

    def act(self):
        self.game.context.board[self.r][self.c] = self.player.index

        self.game.player = None if self.game.context.winning_coords or not self.game.context.empty_coords else \
            self.game.players.next(self.player)
