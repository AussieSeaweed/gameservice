from abc import ABC, abstractmethod


class PokerLimit(ABC):
    @abstractmethod
    def bet_amounts(self, player):
        pass


class PokerLazyNoLimit(PokerLimit):
    def bet_amounts(self, player):
        amounts = []

        if sum(player.relevant for player in player.game.players) > 1:
            max_bet = max(player.bet for player in player.game.players)

            if max_bet + player.game.min_raise < player.total:
                amounts.extend([max_bet + player.game.min_raise, player.total])
            elif max_bet < player.total:
                amounts.append(player.total)

        return amounts


class PokerNoLimit(PokerLazyNoLimit):
    def bet_amounts(self, player):
        amounts = super().bet_amounts(player)

        return list(range(min(amounts), max(amounts) + 1)) if amounts else []
