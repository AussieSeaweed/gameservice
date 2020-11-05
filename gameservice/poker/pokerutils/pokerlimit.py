from abc import ABC, abstractmethod


class PokerLimit(ABC):
    @abstractmethod
    def create_bet_amounts(self, player):
        pass


class PokerNoLimit(PokerLimit):
    def create_bet_amounts(self, player):
        bet_sizes = []

        if max(player.game.bets) + player.game.min_raise <= player.stack + player.bet:
            bet_sizes.extend(range(max(player.game.bets) + player.game.min_raise, player.stack + player.bet + 1))
        elif max(player.game.bets) < player.stack + player.bet:
            bet_sizes.append(player.stack + player.bet)

        return bet_sizes


class PokerLazyNoLimit(PokerLimit):
    def create_bet_amounts(self, player):
        bet_sizes = []

        if max(player.game.bets) + player.game.min_raise <= player.stack + player.bet:
            bet_sizes.extend([max(player.game.bets) + player.game.min_raise, player.stack + player.bet])
        elif max(player.game.bets) < player.stack + player.bet:
            bet_sizes.append(player.stack + player.bet)

        return bet_sizes
