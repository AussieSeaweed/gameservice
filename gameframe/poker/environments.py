from gameframe.game import Environment


class PokerEnvironment(Environment):
    """PokerEnvironment is the class for poker environments."""

    def __init__(self, game):
        super().__init__(game)

        self._aggressor = None
        self._board_cards = []
        self._max_delta = None
        self._requirement = 0

    @property
    def board_cards(self):
        """
        :return: the board cards of this poker environment
        """
        return tuple(self._board_cards)

    @property
    def pot(self):
        """
        :return: the pot of this poker environment
        """
        if self.game.is_terminal:
            return 0
        else:
            return sum(min(player._commitment, self._requirement) for player in self.game.players)

    @property
    def _information(self):
        return {
            **super()._information,
            'board_cards': self.board_cards,
            'pot': self.pot,
        }
