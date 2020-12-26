"""
This module defines functions for interacting with games and sequential games in gameframe.
"""
from json import dumps


def sequential_interact(sequential_game_factory):
    """
    Interacts with sequential games on console.

    :param sequential_game_factory: a function that creates a sequential game instance
    :return: None
    """
    sequential_game = sequential_game_factory()

    while not sequential_game.terminal:
        print(dumps(sequential_game.player.info_set.serialize(), indent=4))

        actions = sequential_game.player.actions

        for i, action in enumerate(actions):
            print(f'{i}: {action}')

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    print(dumps(
        (sequential_game.players[0] if sequential_game.nature is None else sequential_game.nature).info_set.serialize(),
        indent=4))
