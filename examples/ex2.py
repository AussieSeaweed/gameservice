from random import sample

from gameframe.poker import NLTHEGame
from gameframe.utils import pprint

game = NLTHEGame(1, [1, 2], [0, 4, 0, 6])

game.nature.setup()

for player in game.players:
    game.nature.deal_player(player, *sample(game.env.deck, 2))

game.env.actor.fold()

game.nature.deal_board(*sample(game.env.deck, 3))
game.nature.deal_board(*sample(game.env.deck, 1))
game.nature.deal_board(*sample(game.env.deck, 1))

game.env.actor.showdown()
game.env.actor.showdown()
game.env.actor.showdown()

#game.nature.distribute()

pprint(game)
