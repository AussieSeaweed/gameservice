"""This is a sample rock paper scissors game."""
from gameframe.rps import RPSGame, RPSHand

game = RPSGame()
x, y = game.players

x.throw(RPSHand.ROCK)
y.throw(RPSHand.PAPER)

print('Hands:', str(x.hand), str(y.hand))

if game.winner is None:
    winner = 'None'
else:
    winner = 'First' if x is game.winner else 'Second'

print(f'Winner: {winner}')
