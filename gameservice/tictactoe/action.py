from .exception import TTTCellException
from ..game import GameActionArgumentException, SeqAction


class TTTMarkAction(SeqAction):
    def __init__(self, player, r, c):
        super().__init__(player)

        self.__r = r
        self.__c = c

    def _validate(self):
        super()._validate()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise GameActionArgumentException('The cell coordinates are invalid')
        elif self.game.board[self.__r][self.__c] is not None:
            raise TTTCellException('The cell is already occupied')

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
        return f'Mark row {self.__r} column {self.__c}'
