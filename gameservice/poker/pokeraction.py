from abc import ABC
from collections import defaultdict

from ..game import GameActionArgumentException, GameActionException, SequentialAction


class PokerAction(SequentialAction, ABC):
    @property
    def public(self):
        return True

    @property
    def opener(self):
        if any(player.bet for player in self.game.players):
            return self.game.players[1 if len(self.game.players) == 2 else 2]
        else:
            try:
                return next(player for player in self.game.players if player.relevant)
            except StopIteration:
                return self.game.nature

    def open(self):
        self.game.player = self.opener

        if self.game.player.nature:
            self.game.streets.pop(0)
        else:
            self.game.aggressor = self.game.player
            self.game.min_raise = max(self.game.blinds)

    def close(self):
        self.game.player = self.game.nature
        self.game.streets.pop(0)
        self.game.min_raise = None
        self.game.pot += sum(player.bet for player in self.game.players)

        for player in self.game.players:
            player.bet = 0


# Poker Player Actions


class PokerSubmissiveAction(PokerAction):
    def __init__(self, player):
        super().__init__(player)

        if not player.bet < max(player.bet for player in self.game.players):
            raise GameActionException('Cannot fold when the player has bet nothing')

    def act(self):
        super().act()

        self.player.hole_cards = None

        if sum(not player.mucked for player in self.game.players) == 1:
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
        return 'Fold'


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
        return min(self.player.stack, max(player.bet for player in self.game.players) - self.player.bet)

    @property
    def chance(self):
        return False

    def __str__(self):
        return f'Call {self.__amount}' if self.__amount else 'Check'


class PokerAggressiveAction(PokerAction):
    def __init__(self, player, amount):
        super().__init__(player)

        if not (isinstance(amount, int) and sum(player.relevant for player in self.game.players) > 1 and
                (max(player.bet for player in self.game.players) + self.game.min_raise <= amount <= player.total or
                 max(player.bet for player in self.game.players) < amount == player.total)):
            raise GameActionArgumentException('The supplied raise or bet size is not allowed')

        self.__amount = amount

    def act(self):
        super().act()

        self.game.min_raise = max(self.game.min_raise, self.__amount - max(player.bet for player in self.game.players))

        self.player.stack -= self.__amount - self.player.bet
        self.player.bet = self.__amount

        self.game.aggressor = self.player
        self.game.player = next(self.player)

    @property
    def chance(self):
        return False

    def __str__(self):
        return ('Raise ' if any(player.bet for player in self.game.players) else 'Bet ') + str(self.__amount)


# Poker Nature Actions


class PokerStreetAction(PokerAction):
    def __init__(self, player):
        super().__init__(player)

        if self.game.street is None:
            raise GameActionException('You have to do showdown here')

    def act(self):
        super().act()

        for player in self.game.players:
            if not player.mucked:
                player.hole_cards.extend(self.game.deck.draw(self.game.street.num_hole_cards))

        self.game.board.extend(self.game.deck.draw(self.game.street.num_board_cards))

        self.open()

    @property
    def chance(self):
        return True

    def __str__(self):
        return f'Deal {self.game.street.num_hole_cards} hole cards and {self.game.street.num_board_cards} board cards'


class PokerShowdownAction(PokerAction):
    def __init__(self, player):
        super().__init__(player)

        if self.game.street is not None:
            raise GameActionException('You cannot do showdown here')

    def act(self):
        super().act()

        if sum(not player.mucked for player in self.game.players) > 1:
            self.show()

        self.distribute()

        self.game.player = None

    def show(self):
        players = self.game.players[self.game.aggressor.index:] + self.game.players[:self.game.aggressor.index]
        commitments = defaultdict(lambda: 0)

        for player in filter(lambda player: not player.mucked, players):
            for hand, commitment in commitments.items():
                if hand < player.hand and commitment >= player.commitment:
                    player.hole_cards = None
                    break
            else:
                commitments[player.hand] = max(commitments[player.hand], player.commitment)

    def distribute(self):
        players = [player for player in self.game.players if not player.mucked]
        baseline = 0

        for cur_player in sorted(players, key=lambda player: (player.hand, player.commitment)):
            side_pot = 0

            for player in self.game.players:
                entitlement = min(player.commitment, cur_player.commitment)

                if baseline < entitlement:
                    side_pot += entitlement - baseline

            cur_players = [player for player in players if player.hand == cur_player.hand]

            for player in cur_players:
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
        return 'Showdown'
