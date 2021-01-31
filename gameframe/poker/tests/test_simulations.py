from gameframe.poker import NLTexasHEGame

game = NLTexasHEGame(1, [1, 2], [200, 300, 200])


def p() -> None:
    for player in game.players:
        print(player)

    print(game.env)
    print(game.env.actor)
