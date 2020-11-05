from abc import ABC
from collections import defaultdict

from ..game import SequentialAction, GameActionException, GameActionArgumentException


class PokerAction(SequentialAction, ABC):
    @property
    def public(self):
        return True

    @property
    def opener(self):
        try:
            if any(player.bet for player in self.game.players):
                return self.game.players[1 if len(self.game.players) == 2 else 2]
            else:
                return next(player for player in self.game.players if player.relevant)
        except StopIteration:
            return self.game.nature

    def open(self):
        self.game.player = self.opener

        if self.game.player.nature:
            self.game.streets.pop(0)
        else:
            self.game.aggressor = self.game.player

    def close(self):
        self.game.player = self.game.nature
        self.game.streets.pop(0)

        self.game.min_raise = max(self.game.blinds)
        self.game.pot += sum(self.game.bets)

        for player in self.game.players:
            player.bet = 0


# Poker Player Actions


class PokerSubmissiveAction(PokerAction):
    def __init__(self, player):
        super().__init__(player)

        if not player.bet < max(self.game.bets):
            raise GameActionException("Cannot fold when the player has bet nothing")

    def act(self):
        super().act()

        self.player.hole_cards = None

        if sum(player.hole_cards is not None for player in self.game.players) == 1:
            self.close()
            self.game.streets.clear()
        else:
            self.game.player = next(self.player)

            if self.game.player.nature:
                self.close()

    @property
    def chance(self):
        return False

    def __str__(self):
        return "Fold"


class PokerPassiveAction(PokerAction):
    def act(self):
        super().act()

        amount = self.__amount

        self.player.stack -= amount
        self.player.bet += amount

        self.game.player = next(self.player)

        if self.game.player.nature:
            self.close()

    @property
    def __amount(self):
        return min(self.player.stack + self.player.bet, max(self.game.bets)) - self.player.bet

    @property
    def chance(self):
        return False

    def __str__(self):
        return f"Call {self.__amount}" if self.__amount else "Check"


class PokerAggressiveAction(PokerAction):
    def __init__(self, player, amount):
        super().__init__(player)

        if not (isinstance(amount, int) and sum(player.relevant for player in self.game.players) > 1 and
                (max(self.game.bets) + self.game.min_raise <= amount <= player.stack + player.bet or
                 max(self.game.bets) < amount == player.stack + player.bet)):
            raise GameActionArgumentException("The supplied raise or bet size is not allowed")

        self.__amount = amount

    def act(self):
        super().act()

        self.game.min_raise = max(self.game.min_raise, self.__amount - max(self.game.bets))

        self.player.stack -= self.__amount - self.player.bet
        self.player.bet = self.__amount

        self.game.aggressor = self.player
        self.game.player = next(self.player)

    @property
    def chance(self):
        return False

    def __str__(self):
        return f"{'Raise' if self.player.bet else 'Bet'} {self.__amount}"


# Poker Nature Actions


class PokerStreetAction(PokerAction):
    def __init__(self, player):
        super().__init__(player)

        if self.game.street is None:
            raise GameActionException("You have to do showdown here")

    def act(self):
        super().act()

        for player in self.game.players:
            if player.hole_cards is not None:
                player.hole_cards.extend(self.game.deck.draw(self.game.street.num_hole_cards))

        self.game.board.extend(self.game.deck.draw(self.game.street.num_board_cards))

        self.open()

    @property
    def chance(self):
        return True

    def __str__(self):
        return f"Deal {self.game.street.num_hole_cards} hole cards and {self.game.street.num_board_cards} board cards"


class PokerShowdownAction(PokerAction):
    def act(self):
        super().act()

        if sum(player.hole_cards is not None for player in self.game.players) > 1:
            self.show()

        self.distribute()
        self.game.player = None

    def show(self):
        commitments = defaultdict(lambda: 0)

        for player in (player for player in
                       self.game.players[self.game.aggressor.index:] + self.game.players[:self.game.aggressor.index] if
                       player.hole_cards is not None):
            for hand_rank, commitment in commitments.items():
                if hand_rank < player.hand_rank and commitment >= player.commitment:
                    player.hole_cards = None
                    break
            else:
                player.exposed = True
                commitments[player.hand_rank] = max(commitments[player.hand_rank], player.commitment)

    def distribute(self):
        assert all(player.stack >= 0 for player in self.game.players)

        players = [player for player in self.game.players if player.hole_cards is not None]
        baseline = 0

        for cur_player in sorted(players, key=lambda player: (player.hand_rank, player.commitment)):
            side_pot = 0

            for player in self.game.players:
                if baseline < min(player.commitment, cur_player.commitment):
                    side_pot += min(player.commitment, cur_player.commitment) - baseline

            for player in (cur_players := [player for player in players if player.hand_rank == cur_player.hand_rank]):
                player.bet += side_pot // len(cur_players)
            else:
                cur_players[0].bet += side_pot % len(cur_players)

            baseline = max(baseline, cur_player.commitment)

        self.game.pot = 0

        for player in players:
            player.stack += player.bet
            player.bet = 0

    @property
    def chance(self):
        return True

    def __str__(self):
        return "Showdown"
