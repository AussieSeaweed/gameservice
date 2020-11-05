from ..game import SequentialAction, GameActionArgumentException


class TicTacToeMarkAction(SequentialAction):
    def __init__(self, player, r, c):
        super().__init__(player)

        if not (0 <= r < 3 and 0 <= c < 3):
            raise GameActionArgumentException("The cell coordinate is invalid")

        self.__r = r
        self.__c = c

    def act(self):
        super().act()

        self.game.board[self.__r][self.__c] = self.player.index
        self.game.player = next(self.player) if self.game.empty_coords and self.game.winner is None else None

    @property
    def chance(self):
        return False

    @property
    def public(self):
        return True

    def __str__(self):
        return f"Mark row {self.__r} column {self.__c}"
