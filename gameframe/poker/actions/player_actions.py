from typing import Union

from gameframe.game import Actor
from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.stages import BettingStage, ShowdownStage


class BettingAction(PokerAction[PokerPlayer]):
    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self._game.env.actor, PokerPlayer) \
               and isinstance(self._game.env._stage, BettingStage)

    def next_actor(self, actor: Actor) -> Union[PokerNature, PokerPlayer]:
        actor = super().next_actor(actor)

        if isinstance(actor, PokerNature) or actor is self._game.env._aggressor:
            return self._game.nature
        elif isinstance(actor, PokerPlayer) and not actor.is_mucked and actor.effective_stack > 0:
            return actor
        else:
            return self.next_actor(actor)

    def close(self) -> None:
        pass


class FoldAction(BettingAction):
    def __str__(self) -> str:
        return 'Fold'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self._actor.bet < max(player.bet for player in self._game.players)

    def act(self) -> None:
        super().act()

        self._actor._muck()

        if sum(not player.is_mucked for player in self._game.players) == 1:
            self._game.env._actor = self._game.nature
        else:
            self._game.env._actor = self.next_actor(self._actor)

            if isinstance(self._game.env._actor, PokerNature):
                self.close()


class CheckCallAction(BettingAction):
    def __str__(self) -> str:
        return f'Call {self.amount}' if self.amount else 'Check'

    @property
    def amount(self) -> int:
        return min(self._actor.stack, max(player.bet for player in self._game.players) - self._actor.bet)

    def act(self) -> None:
        super().act()

        amount = self.amount

        self._actor._bet += amount
        self._actor._stack -= amount

        self._game.env._actor = self.next_actor(self._actor)

        if isinstance(self._game.env._actor, PokerNature):
            self.close()


class BetRaiseAction(BettingAction):
    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self._amount = amount

    def __str__(self) -> str:
        return ('Raise ' if any(player.bet for player in self._game.players) else 'Bet ') + str(self._amount)

    def act(self) -> None:
        super().act()

        self._game.env._aggressor = self._actor
        self._game.env._max_delta = max(self._game.env._max_delta,
                                        self._amount - max(player.bet for player in self._game.players))

        self._actor._stack -= self._amount - self._actor._bet
        self._actor._bet = self._amount

        self._game._actor = self.next_actor(self._actor)


class ShowdownAction(BettingAction):
    def __init__(self, game: PokerGame, actor: PokerPlayer, force: bool):
        super().__init__(game, actor)

        self._force = force

    def __str__(self) -> str:
        return 'Showdown'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self._game.env.actor, PokerPlayer) \
               and isinstance(self._game.env._stage, ShowdownStage) and not self._actor.is_mucked
