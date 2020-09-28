from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, game, index):
        self.game = game
        self.index = index
        self.label = None if index is None or game.labels is None else game.labels[index]

    @property
    def nature(self):
        return False

    @property
    def actions(self):
        return self.game.player_actionset_type(self.game, self)

    @property
    def public_info(self):
        return {
            "index": self.index,
            "label": self.label,
        }

    @property
    def private_info(self):
        return self.public_info

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
        return self.game.nature_actionset_type(self.game, self)

    def __str__(self):
        return "Nature"
