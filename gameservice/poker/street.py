from ..game.actions import EmtpyActions
from .actions import BettingActions, DealActions, PeelActions, ResultActions


class Street:
    player_actions_type = None
    nature_actions_type = None
    order = None

    def __init__(self, game):
        self.game = game


class DealStreet(Street):
    player_actions_type = BettingActions
    nature_actions_type = DealActions

    num_cards = None

    @property
    def order(self):
        return [None, *self.player_order]

    @property
    def player_order(self):
        return [i for i in range(self.game.num_players) if not self.game.players[i].mucked]


class PeelStreet(Street):
    player_actions_type = BettingActions
    nature_actions_type = PeelActions

    num_cards = None

    @property
    def order(self):
        return [None, *self.player_order]

    @property
    def player_order(self):
        return [i for i in range(self.game.num_players) if not self.game.players[i].mucked]


class ResultStreet(Street):
    player_actions_type = EmtpyActions
    nature_actions_type = ResultActions
    order = [None]

    evaluate = None
