from gameframe.poker import NLTexasHEGame

game = NLTexasHEGame(1, [1, 2], [200, 300, 200])


def a():
    return game.env.actor


def p():
    for player in game.players:
        print(player)

    print(game.env)
    print(game.env.actor)
    print(game.env._stage.__class__.__name__)


a().setup()
a().deal_player(game.players[0], 'Qd', 'Qh')
a().deal_player(game.players[1], 'Ah', 'Kh')
a().deal_player(game.players[2], 'Jd', 'Tc')
a().bet_raise(6)
a().check_call()
a().bet_raise(18)
a().check_call()
a().check_call()
a().deal_board('Ad', 'Qc', 'Ks')
a().check_call()
a().check_call()
a().bet_raise(181)
a().check_call()
a().check_call()
a().deal_board('Ac')
a().deal_board('2h')
a().showdown()
a().showdown()
a().showdown()
a().distribute()

p()
