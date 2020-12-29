from ..game import Environment


class PokerEnvironment(Environment):
    """PokerEnvironment is the class for poker environments."""

    def __init__(self, game):
        super().__init__(game)

        self.__board = []
        self._pot = 0

        self._aggressor = None
        self._max_delta = None

    @property
    def board(self):
        """
        :return: the board of the poker environment
        """
        return self.__board

    @property
    def pot(self):
        """
        :return: the pot of the poker environment
        """
        return self._pot

    @property
    def _information(self):
        return {
            **super()._information,
            'pot': self.pot,
            'board': self.board,
        }
