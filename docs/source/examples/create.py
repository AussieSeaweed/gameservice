from gameframe.poker import KuhnGame, NLGGame, NLOGame, NLSGame, NLTGame, PLGGame, PLOGame, PLSGame, PLTGame
from gameframe.rockpaperscissors import RPSGame
from gameframe.tictactoe import TTTGame

ante = 1
blinds = [1, 2]
button_blind = 2
starting_stacks = [200, 200, 300]

# Create a No-Limit Texas Hold'em game
nlt_game = NLTGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Texas Hold'em game
plt_game = PLTGame(ante, blinds, starting_stacks)

# Create a No-Limit Omaha Hold'em game
nlo_game = NLOGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Omaha Hold'em game
plo_game = PLOGame(ante, blinds, starting_stacks)

# Create a No-Limit Greek Hold'em game
nlg_game = NLGGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Greek Hold'em game
plg_game = PLGGame(ante, blinds, starting_stacks)

# Create a No-Limit Short-Deck Hold'em game
nls_game = NLSGame(ante, button_blind, starting_stacks)

# Create a Pot-Limit Short-Deck Hold'em game
pls_game = PLSGame(ante, button_blind, starting_stacks)

# Create a Kuhn Poker game
kuhn_game = KuhnGame()

# Create a tic tac toe game
ttt_game = TTTGame()

# Create a rock paper scissors game
rps_game = RPSGame()
