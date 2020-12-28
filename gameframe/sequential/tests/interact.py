def sequential_interact(sequential_game_factory):
    """Interacts with sequential games on console.

    :param sequential_game_factory: a function that creates a sequential game instance
    :return: None
    """
    sequential_game = sequential_game_factory()

    while not sequential_game.terminal:
        print(sequential_game.player.info_set)

        actions = sequential_game.player.actions

        for i, action in enumerate(actions):
            print(f'{i}: {action}')

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    print(sequential_game.nature.info_set)
