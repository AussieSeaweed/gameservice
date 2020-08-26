class Street:
    player_actions_type = None
    nature_actions_type = None
    order = None

    def __init__(self, game):
        self.game = game


class DealStreet(Street):
    num_cards = None


class PeelStreet(Street):
    num_cards = None


class Showdown(Street):
    evaluate = None
