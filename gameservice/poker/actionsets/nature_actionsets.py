from gameservice.game.actionsets import CachedActionSet
from ..actions import Peel, Showdown, Distribute, Deal


class PreFlop(Deal):
    def __init__(self, game, player, num_cards=0):
        super().__init__(game, player, num_cards)

    @property
    def opener(self):
        player = self.game.players[1 if self.game.num_players == 2 else 2]

        if not player.relevant:
            player = self.game.players.next_relevant(player)

        return player


class FTRNatureActionSet(CachedActionSet):
    num_preflop_cards = None

    def _create_actions(self):
        actions = []

        if self.game.player is self.player:
            if self.game.context.street == 0:
                actions.append(PreFlop(self.game, self.player, self.num_preflop_cards))
            elif self.game.context.street == 1:
                actions.append(Peel(self.game, self.player, 3))
            elif self.game.context.street == 2 or self.game.context.street == 3:
                actions.append(Peel(self.game, self.player, 1))
            elif self.game.context.street == 4:
                actions.append(Showdown(self.game, self.player))
            else:
                actions.append(Distribute(self.game, self.player))

        return actions
