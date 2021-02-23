"""This shows the 800K dollar pot played between Xuan and Phua.

Video: https://www.youtube.com/watch?v=QlgCcphLjaQ
"""
from pokertools import parse_cards

from gameframe.poker import NLSGame

game = NLSGame(3000, 3000, [495000, 232000, 362000, 403000, 301000, 204000])
badziakouski, zhong, xuan, jun, phua, koon = game.players

# Pre-flop

game.nature.deal_player(badziakouski, parse_cards('Th8h'))
game.nature.deal_player(zhong, parse_cards('QsJd'))
game.nature.deal_player(xuan, parse_cards('QhQd'))
game.nature.deal_player(jun, parse_cards('8d7c'))
game.nature.deal_player(phua, parse_cards('KhKs'))
game.nature.deal_player(koon, parse_cards('8c7h'))

badziakouski.check_call()
zhong.check_call()
xuan.bet_raise(35000)
jun.fold()
phua.bet_raise(298000)
koon.fold()
badziakouski.fold()
zhong.fold()
xuan.check_call()

# Flop

game.nature.deal_board(parse_cards('9h6cKc'))

# Turn

game.nature.deal_board(parse_cards('Jh'))

# River

game.nature.deal_board(parse_cards('Ts'))

# Pot: 623000

print(f'Pot: {game.pot}')

phua.showdown()
xuan.showdown()

print('Players:')
print('\n'.join(map(str, game.players)))
print('Board:', ''.join(map(str, game.board_cards)))
