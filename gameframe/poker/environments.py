from gameframe.game import Environment


class PokerEnvironment(Environment):
    """PokerEnvironment is the class for poker environments."""

    def __init__(self, game):
        super().__init__(game)

        self.max_delta = None

        self.__board_cards = []
        self.__pots = []

    @property
    def board_cards(self):
        """
        :return: the board cards of the poker environment
        """
        return self.__board_cards

    @property
    def pot(self):
        """
        :return: the pot of the poker environment
        """
        return sum(self.game.starting_stacks) - sum(player.total for player in self.game.players)

    @property
    def information(self):
        return {
            **super().information,
            'board_cards': self.board_cards,
            'pot': self.pot,
        }
