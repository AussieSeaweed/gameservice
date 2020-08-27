from ..exceptions import InvalidActionArgumentException, InvalidActionException
from ..sequential.action import SequentialAction


class AggressiveAction(SequentialAction):
    def __init__(self, game, player, amount):
        super().__init__(game, player)

        if not (isinstance(amount, int) and
                (max(game.players.bets) + game.context.min_raise <= amount <= player.total or
                 max(game.players.bets) < amount == player.total)):
            raise InvalidActionArgumentException

        self.__amount = amount

    @property
    def label(self):
        return f"{'Raise' if max(self.game.players.bets) else 'Bet'} {self.__amount}"

    def act(self):
        pass


class PassiveAction(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return f"Call {max(self.game.players.bets) - self.player.bet}" if max(self.game.players.bets) else "Check"

    def act(self):
        pass


class YieldingAction(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

        if max(game.players.bets) == player.bet:
            raise InvalidActionException

    @property
    def label(self):
        return "Fold"

    def act(self):
        pass


class Deal(SequentialAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.__num_cards = num_cards

    @property
    def label(self):
        return f"Deal {self.__num_cards} cards"

    def act(self):
        pass


class Peel(SequentialAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.__num_cards = num_cards

    @property
    def label(self):
        return "Peel"

    def act(self):
        pass


class Showdown(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return "Showdown"

    def act(self):
        pass


class Distribute(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return "Distribute"

    def act(self):
        if not self.game.winners:
            self.game.winners = [player for player in self.game.players if not player.mucked]

        self.game.winners[0].stack += self.game.context.pot % len(self.game.winners)

        for winner in self.game.winners:
            winner.stack += self.game.context.pot // len(self.game.winners)

        self.game.context.pot = 0
