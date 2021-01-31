from gameframe.poker import NLTexasHEGame

game = NLTexasHEGame(1, [1, 2], [200, 300, 200])


def p():
    for player in game.players:
        print(player)

    print(game.env)
    print(game.env.actor)


game.env.actor.actions[0].act()
