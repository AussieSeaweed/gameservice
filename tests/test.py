def print_infoset(player):
    for key, value in player.infoset.items():
        if type(value) is dict:
            print(f"{key}: ")

            for u, v in value.items():
                print(f"{u}: {v}")
        elif type(value) is list:
            print(f"{key}: ")

            for u, v in enumerate(value):
                print(f"{u}: {v}")
        else:
            print(f"{key}: {value}")


def interactive_test(game_type):
    game = game_type()

    while not game.terminal:
        print_infoset(game.player)

        try:
            choice = list(game.player.actions)[0 if game.player.nature else int(input(f"\n{game.player} action: "))]
            print(f"\nYou chose: {choice}\n\n")
            game.player.actions[choice].act()
        except IndexError:
            print("\nError Try again\n")

    print_infoset(game.players.nature)

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
