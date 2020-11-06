from abc import ABC, abstractmethod


class PokerLimit(ABC):
    @abstractmethod
    def bet_amounts(self, player):
        pass


class PokerNoLimit(PokerLimit):
    def bet_amounts(self, player):
        bet_sizes = []

        if max(player.game.bets) + player.game.min_raise <= player.total:
            bet_sizes.extend(range(max(player.game.bets) + player.game.min_raise, player.total + 1))
        elif max(player.game.bets) < player.total:
            bet_sizes.append(player.total)

        return bet_sizes


class PokerLazyNoLimit(PokerLimit):
    def bet_amounts(self, player):
        bet_sizes = []

        if max(player.game.bets) + player.game.min_raise <= player.total:
            bet_sizes.extend([max(player.game.bets) + player.game.min_raise, player.total])
        elif max(player.game.bets) < player.total:
            bet_sizes.append(player.total)

        return bet_sizes
