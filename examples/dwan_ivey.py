"""
This shows the 1.1 million dollar pot played between Dwan and Ivey

Video: https://www.youtube.com/watch?v=GnxFohpljqM
"""

from gameframe.poker import NLTHEGame
from gameframe.utils import pprint

game = NLTHEGame(500, [1000, 2000], [1125600, 2000000, 553500])  # Antonius's stack is unknown
ivey, antonius, dwan = game.players

game.nature.setup()

# Pre-flop

game.nature.deal_player(ivey, 'Ac', '2d')
game.nature.deal_player(antonius, '5h', '7s')  # Unknown
game.nature.deal_player(dwan, '7h', '6h')

dwan.bet_raise(6000)  # Unknown
ivey.bet_raise(23000)
antonius.fold()
dwan.check_call()

# Flop

game.nature.deal_board('Jc', '3d', '5c')

ivey.bet_raise(35000)
dwan.check_call()

# Turn

game.nature.deal_board('4h')

ivey.bet_raise(90000)
dwan.bet_raise(232600)
ivey.bet_raise(1067100)
dwan.check_call()

# River

game.nature.deal_board('Jh')

ivey.showdown()
dwan.showdown()

# Pot: 1108500

game.nature.distribute()

pprint(game)
