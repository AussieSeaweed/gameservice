from collections.abc import Sequence
from typing import Type

from gameframe.poker import NoLimitGreekHoldEmGame, NoLimitOmahaHoldEmGame, NoLimitTexasHoldEmGame, PokerGame
from gameframe.sequential.tests import interact_sequential

__all__ = ['interact_poker']


def interact_poker() -> None:
    """Interacts with a poker game."""
    game_types: Sequence[Type[PokerGame]] = [
        NoLimitTexasHoldEmGame,
        NoLimitGreekHoldEmGame,
        NoLimitOmahaHoldEmGame,
    ]

    print('Choose a game: ')

    for i, game_type in enumerate(game_types):
        print(f'{i}: {game_type.__name__}')

    i: int = int(input('Game #: '))

    ante: int = int(input('Ante: '))
    blinds: Sequence[int] = list(map(int, input('Blinds: ').split()))
    starting_stacks: Sequence[int] = list(map(int, input('Starting stacks: ').split()))

    interact_sequential(lambda: game_types[i](ante, blinds, starting_stacks, True))


if __name__ == '__main__':
    interact_poker()
