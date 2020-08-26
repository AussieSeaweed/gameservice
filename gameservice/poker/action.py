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
    def __init__(self, game, player, index, num_cards):
        super().__init__(game, player)

        try:
            if not game.players.nature or self.game.players[index].mucked or num_cards <= 0:
                raise InvalidActionArgumentException
        except (IndexError, TypeError):
            raise InvalidActionArgumentException

        self.__index = index
        self.__num_cards = num_cards

    @property
    def label(self):
        return f"Deal {self.__num_cards} cards to Player {self.__index}"

    def act(self):
        pass


class Showdown(SequentialAction):
    def __init__(self, game, player, index):
        super().__init__(game, player)

        try:
            if not game.players.nature or self.game.players[index].mucked:
                raise InvalidActionArgumentException
        except (IndexError, TypeError):
            raise InvalidActionArgumentException

        self.__index = index

    @property
    def label(self):
        return f"Showdown Player {self.__index}"

    def act(self):
        pass


class Distribute(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return "Distribute"

    def act(self):
        pass
