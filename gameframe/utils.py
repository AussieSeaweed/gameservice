from gameframe.game import Game
from gameframe.game.bases import E, N, P


def next_player(game: Game[E, N, P], player: P) -> P:
    if player.is_nature:
        return player
    else:
        return game.players[(game.players.index(player) + 1)
                            % len(game.players)]
