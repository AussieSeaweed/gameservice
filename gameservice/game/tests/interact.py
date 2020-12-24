"""
This module defines functions for interacting with games and sequential games in gameservice.
"""
from json import dumps


def interact_seq(seq_game_factory):
    """
    Interacts with sequential games on console.

    :param seq_game_factory: a function that creates a sequential game instance
    :return: None
    """
    seq_game = seq_game_factory()

    while not seq_game.terminal:
        print(dumps(seq_game.player.info_set.serialize(), indent=4))

        actions = seq_game.player.actions

        for i, action in enumerate(actions):
            print(f'{i}: {action}')

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    print(dumps((seq_game.players[0] if seq_game.nature is None else seq_game.nature).info_set.serialize(), indent=4))
