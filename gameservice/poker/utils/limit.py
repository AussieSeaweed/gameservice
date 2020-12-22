from abc import ABC, abstractmethod


class Limit(ABC):
    @classmethod
    @abstractmethod
    def bet_amounts(cls, player):
        pass


class NoLimit(Limit):
    @classmethod
    def bet_amounts(cls, player):
        amounts = []

        if sum(player.relevant for player in player.game.players) > 1:
            max_bet = max(player.bet for player in player.game.players)

            if max_bet + player.game.environment.min_raise < player.total:
                amounts.extend(cls.int_bet_amounts(max_bet + player.game.environment.min_raise, player.total))
            elif max_bet < player.total:
                amounts.append(player.total)

        return amounts

    @staticmethod
    def int_bet_amounts(min_amount, max_amount):
        return list(range(min_amount, max_amount + 1))


class LazyNoLimit(NoLimit):
    @staticmethod
    def int_bet_amounts(min_amount, max_amount):
        return list({min_amount, max_amount})
