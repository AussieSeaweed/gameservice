def print_game(game):
    for player in game.players:
        print(player.private_info if player is game.player else player.public_info)

    print(game.context.info)

    if game.player is not None:
        for index, action in enumerate(game.player.actions):
            print(index, action)


def interactive_test(game_type):
    game = game_type()

    while not game.terminal:
        print_game(game)

        try:
            choice = list(game.player.actions)[0 if game.player.nature else int(input(f"\n{game.player} action: "))]
            print(f"\nYou chose: {choice}\n\n")
            game.player.actions[choice].act()
        except IndexError:
            print("\nError Try again\n")

    print_game(game)

    print("payoffs: ", {
        **{i: player.payoff for i, player in enumerate(game.players)},
        None: game.players.nature.payoff
    })


def random_test(game_type, num_tests, step):
    from random import choice

    for i in range(num_tests):
        game = game_type()

        while not game.terminal:
            game.player.actions[choice(list(game.player.actions))].act()

        if i % step == 0:
            print(i // step)

    print("success")
