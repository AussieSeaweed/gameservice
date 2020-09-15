from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, game, index):
        self.game = game
        self.index = index

    @property
    def nature(self):
        return False

    @property
    def actions(self):
        return self.game.player_actions_type(self.game, self)

    @property
    def public_info(self):
        return {}

    @property
    def private_info(self):
        return self.public_info

    @property
    def infoset(self):
        return {
            "players": {
                **{
                    i: player.private_info if self is player else player.public_info for i, player in
                    enumerate(self.game.players)
                },

                None: self.game.players.nature.private_info if self.nature else self.game.players.nature.public_info
            },

            "context": self.game.context.info,
            "actions": list(self.actions),
        }

    @property
    @abstractmethod
    def payoff(self):
        pass

    def __str__(self):
        return f"Player {self.index}"


class Nature(Player, ABC):
    def __init__(self, game):
        super().__init__(game, None)

    @property
    def nature(self):
        return True

    @property
    def actions(self):
        return self.game.nature_actions_type(self.game, self)

    def __str__(self):
        return "Nature"
