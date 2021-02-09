"""This shows the 1.3 million dollar pot played between Antonius and Isildur. Technically, they were playing pot-limit
Omaha Hold'em, but this can nonetheless be simulated as a no-limit Omaha Hold'em hand.

Video: https://www.youtube.com/watch?v=UMBm66Id2AA
"""

from gameframe.poker import NLOHEGame
from decimal import Decimal

game = NLOHEGame(0, [500, 1000], [Decimal('1259450.25'), Decimal('678473.50')])
antonius, isildur = game.players

# Pre-flop

game.nature.deal_player(antonius, 'Ah', '3s', 'Ks', 'Kh')
game.nature.deal_player(isildur, '6d', '9s', '7d', '8h')

isildur.bet_raise(3000)
antonius.bet_raise(9000)
isildur.bet_raise(27000)
antonius.bet_raise(81000)
isildur.check_call()

# Flop

game.nature.deal_board('4s', '5c', '2h')

antonius.bet_raise(91000)
isildur.bet_raise(435000)
antonius.bet_raise(779000)
isildur.check_call()

# Turn and River

game.nature.deal_board('5h')
game.nature.deal_board('9c')

# Pot: 1356947.00 (0.50 was probably collected as rake in the actual game)

antonius.showdown()
isildur.showdown()

print('Players:')
print('\n'.join(map(str, game.players)))
print('Board:', ' '.join(map(str, game.board_cards)))
