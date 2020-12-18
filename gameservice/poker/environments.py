from ..game import Environment


class PokerEnvironment(Environment):
    def __init__(self, game):
        super().__init__(game)

        self.aggressor = None
        self.min_raise = None

        self.pot = 0
        self.__board = []

    @property
    def board(self):
        return self.__board
