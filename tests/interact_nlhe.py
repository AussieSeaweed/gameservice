import json

from gameservice.poker import LazyNLHEGame


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


def interact_nlhe():
    game = TestNLHEGame()

    while not game.terminal:
        print(json.dumps(game.player.info_set.serialize(), indent=4))

        actions = game.player.actions

        for action in actions:
            print(action)

        actions[0 if len(actions) == 1 else int(input('Action index: '))].act()

    print(json.dumps((game.players[0] if game.nature is None else game.nature).info_set.serialize(), indent=4))


if __name__ == '__main__':
    interact_nlhe()
