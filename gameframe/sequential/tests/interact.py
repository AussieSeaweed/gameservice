def pretty_print(o, indent='    ', start='', end='\n'):
    """Prints the object on the console prettily.

    :param o: the object
    :param indent: the indentation string
    :param start: the prefix string
    :param end: the suffix string
    :return: None
    """
    if isinstance(o, dict):
        print(start + '{')

        for key, value in o.items():
            print(start + indent + str(key), end=':\n')
            pretty_print(value, indent, start + indent + indent, end=',\n')

        print(start + '}', end=end)
    elif isinstance(o, list):
        print(start + '[')

        for value in o:
            pretty_print(value, indent, start + indent, end=',\n')

        print(start + ']', end=end)
    else:
        print(start + str(o), end=end)


def interact_sequential(sequential_game_factory):
    """Interacts with a sequential game on the console.

    :param sequential_game_factory: a function that creates the sequential game instance
    :return: None
    """
    game = sequential_game_factory()

    while not game.is_terminal:
        pretty_print(game.actor.information_set)

        actions = game.actor.actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    pretty_print(game.nature.information_set)
