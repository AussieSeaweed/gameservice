from gameservice.poker import LazyNLHEGame
import json


class TestNLHEGame(LazyNLHEGame):
    @property
    def starting_stacks(self):
        return [200, 400, 300]

    @property
    def blinds(self):
        return [1, 2]

    @property
    def ante(self):
        return 0


def interact_sequential_game(sequential_game_type):
    sequential_game = sequential_game_type()

    while not sequential_game.terminal:
        print(json.dumps(sequential_game.player.info_set.serialize(), indent=4))

        actions = sequential_game.player.actions

        for action in actions:
            print(action)

        actions[0 if len(actions) == 1 else int(input('Action index: '))].act()

    print(json.dumps(
        (sequential_game.players[0] if sequential_game.nature is None else sequential_game.nature).info_set.serialize(),
        indent=4,
    ))


if __name__ == '__main__':
    interact_sequential_game(TestNLHEGame)
