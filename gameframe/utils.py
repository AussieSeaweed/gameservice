from typing import TypeVar

from gameframe.game import Actor, Game
from gameframe.game.bases import E, N

P = TypeVar('P', bound=Actor)


def next_player(game: Game[E, N, P], player: P) -> P:
    """Gets the next player in the game.

    :param game: the game
    :param player: the player from which the next player is obtained
    :return: the next player of the supplied player
    """
    return game.players[(game.players.index(player) + 1) % len(game.players)]
