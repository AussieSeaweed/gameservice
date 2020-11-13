from testgames import CustomHUNLHEGame


def interact_sequential_game(sequential_game_type):
    sequential_game = sequential_game_type()

    while not sequential_game.terminal:
        print(sequential_game.player.info_set)

        actions = sequential_game.player.actions

        for action in actions:
            print(action)

        actions[0 if len(actions) == 1 else int(input('Action index: '))].act()

    print((sequential_game.players[0] if sequential_game.nature is None else sequential_game.nature).info_set)


if __name__ == '__main__':
    interact_sequential_game(CustomHUNLHEGame)
