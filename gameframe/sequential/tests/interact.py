from gameframe.utils import pretty_print


def interact_sequential(sequential_game_factory):
    """Interacts with a sequential game on the console.

    :param sequential_game_factory: a function that creates the sequential game instance
    :return: None
    """
    game = sequential_game_factory()

    while not game.terminal:
        pretty_print(game.actor.information_set)

        actions = game.actor.actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    pretty_print(game.nature.information_set)
