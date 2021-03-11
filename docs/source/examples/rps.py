"""This is a sample rock paper scissors game."""
from gameframe.rps import RPSGame, RPSHand

game = RPSGame()
x, y = game.players

x.throw(RPSHand.ROCK)
y.throw(RPSHand.PAPER)
