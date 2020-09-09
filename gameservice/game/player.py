class Player:
    payoff = None

    def __init__(self, game):
        self.game = game

    @property
    def nature(self):
        return False

    @property
    def actions(self):
        return self.game.player_actions_type(self.game, self)

    @property
    def public_info(self):
        return {
            "payoff": self.payoff,
            "active": len(self.actions) > 0,
        }

    @property
    def private_info(self):
        return self.public_info

    @property
    def infoset(self):
        return {
            "players": [player.private_info if self is player else player.public_info for player in self.game.players],
            "context": self.game.context.info,
            "actions": list(self.actions),
            "logs": self.game.logs,
        }

    @property
    def index(self):
        return self.game.players.index(self)

    def __str__(self):
        return f"Player {self.game.players.index(self)}"


class Nature(Player):
    @property
    def nature(self):
        return True

    @property
    def actions(self):
        return self.game.nature_actions_type(self.game, self)

    def __str__(self):
        return "Nature"
