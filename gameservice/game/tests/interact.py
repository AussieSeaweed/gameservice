from json import dumps


def interact_seq(game_factory):
    game = game_factory()

    while not game.terminal:
        print(dumps(game.player.info_set.serialize(), indent=4))

        actions = game.player.actions

        for i, action in enumerate(actions):
            print(f'{i}: {action}')

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    print(dumps((game.players[0] if game.nature is None else game.nature).info_set.serialize(), indent=4))
