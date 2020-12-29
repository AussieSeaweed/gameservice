from gameframe.game.tests import pretty_print


def sequential_interact(sequential_game_factory):
    """Interacts with sequential games on console.

    :param sequential_game_factory: a function that creates a sequential game instance
    :return: None
    """
    sequential_game = sequential_game_factory()

    while not sequential_game.terminal:
        pretty_print(sequential_game.player.information_set)

        actions = sequential_game.player.actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    pretty_print(sequential_game.nature.information_set)
