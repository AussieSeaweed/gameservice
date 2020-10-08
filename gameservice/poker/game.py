from .actionset import PokerPlayerActionSet
from .context import PokerContext
from .players import PokerPlayer, PokerNature
from .playerset import PokerPlayerSet
from ..exceptions import PlayerNumException
from ..sequential.game import SequentialGame


class PokerGame(SequentialGame):
    player_type = PokerPlayer
    nature_type = PokerNature
    context_type = PokerContext

    playerset_type = PokerPlayerSet

    player_actionset_type = PokerPlayerActionSet

    """Poker variables"""

    deck_type = None
    evaluator_type = None

    ante = None
    blinds = None
    starting_stacks = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.num_players < 2:
            raise PlayerNumException("Poker requires 2 or more players")

        self.deck = self.deck_type()
        self.evaluator = self.evaluator_type()

        if self.ante is not None:
            for player in self.players:
                ante = min(self.ante, player.stack)

                player.stack -= ante
                self.context.pot += ante

        if self.blinds is not None:
            for player, blind in zip(reversed(self.players) if len(self.players) == 2 else self.players, self.blinds):
                blind = min(blind, player.stack)

                player.stack -= blind
                player.bet += blind

    def _get_initial_player(self):
        return self.players.nature

    @property
    def num_players(self):
        return len(self.starting_stacks)

    def evaluate(self, card_str_list):
        return self.evaluator.evaluate(card_str_list)

    def bet_sizes(self, min_raise, max_raise):
        return range(min_raise, max_raise + 1)
