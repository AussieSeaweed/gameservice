from ..game import Player


class PokerPlayer(Player):
    """PokerPlayer is the class for poker players."""

    @property
    def actions(self):
        pass

    @property
    def payoff(self):
        return 0


class PokerNature(Player):
    """PokerNature is the class for poker natures."""

    @property
    def actions(self):
        pass

    @property
    def payoff(self):
        return 0
