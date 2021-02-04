from typing import Sequence, TypeVar

from gameframe.game import BaseGame
from gameframe.sequential import BaseSeqGame

T = TypeVar('T')


def rotate(s: Sequence[T], i: int) -> Sequence[T]:
    return list(s[i:]) + list(s[:i])


def pprint(game: BaseGame) -> None:
    for i, player in enumerate(game.players):
        print(f'Player {i}: {player}')

    print(f'Env: {game.env}')

    if isinstance(game, BaseSeqGame):
        print(f'Actor: {game.actor}')
