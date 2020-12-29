from ..sequential import SequentialAction


class MarkAction(SequentialAction):
    """MarkAction is the class for mark actions."""

    def __init__(self, player, r, c):
        super().__init__(player)

        self.__r = r
        self.__c = c

    def act(self):
        super().act()

        self.game.environment.board[self.__r][self.__c] = self.player

        if self.game.environment._empty_coordinates and self.game.environment._winner is None:
            self.game._player = next(self.player)
        else:
            self.game._player = None

    @property
    def chance(self):
        return False

    @property
    def public(self):
        return True

    def __str__(self):
        return f'Mark row {self.__r} column {self.__c}'

    def _verify(self):
        super()._verify()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise ValueError('The cell coordinates are out of range')
        elif self.game.environment.board[self.__r][self.__c] is not None:
            raise ValueError('The cell is already occupied')
