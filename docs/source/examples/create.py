from gameframe.poker import NLTHEGame, NLOHEGame, NLGHEGame
from gameframe.tictactoe import TTTGame

ante = 1
blinds = [1, 2]
starting_stacks = [200, 200, 300]

# Create a no-limit Texas Hold'em game
nlthe_game = NLTHEGame(ante, blinds, starting_stacks)

# Create a no-limit Omaha Hold'em game
nlohe_game = NLOHEGame(ante, blinds, starting_stacks)

# Create a no-limit Greek Hold'em game
nlghe_game = NLGHEGame(ante, blinds, starting_stacks)

# Create a tic tac toe game
ttt_game = TTTGame()
