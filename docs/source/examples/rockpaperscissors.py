"""This is a sample rock paper scissors game."""
from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand

game = RockPaperScissorsGame()
x, y = game.players

x.throw(RockPaperScissorsHand.ROCK)
y.throw(RockPaperScissorsHand.PAPER)
