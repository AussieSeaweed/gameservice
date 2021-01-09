from gameframe.poker import NoLimitGreekHoldEmGame, NoLimitOmahaHoldEmGame, NoLimitTexasHoldEmGame
from gameframe.sequential.tests import interact_sequential


def interact_poker():
    """Interacts with a poker game."""
    game_types = [
        NoLimitTexasHoldEmGame,
        NoLimitGreekHoldEmGame,
        NoLimitOmahaHoldEmGame,
    ]

    print('Choose a game: ')

    for i, game_type in enumerate(game_types):
        print(f'{i}: {game_type.__name__}')

    i = int(input('Game #: '))

    ante = int(input('Ante: '))
    blinds = list(map(int, input('Blinds: ').split()))
    starting_stacks = list(map(int, input('Starting stacks: ').split()))

    interact_sequential(lambda: game_types[i](ante, blinds, starting_stacks, True))


if __name__ == '__main__':
    interact_poker()
