from gameframe.poker import (FLGGame, FLO5Game, FLOGame, FLSGame, FLTGame, KuhnGame, NLGGame, NLO5Game, NLOGame,
                             NLSGame, NLTGame, PLGGame, PLO5Game, PLOGame, PLSGame, PLTGame)
from gameframe.rockpaperscissors import RPSGame
from gameframe.tictactoe import TTTGame

ante = 1
blinds = [1, 2]
button_blind = 2
starting_stacks = [200, 200, 300]

# Create a Fixed-Limit Texas Hold'em game
flt_game = FLTGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Texas Hold'em game
plt_game = PLTGame(ante, blinds, starting_stacks)

# Create a No-Limit Texas Hold'em game
nlt_game = NLTGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit Omaha Hold'em game
flo_game = FLOGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Omaha Hold'em game
plo_game = PLOGame(ante, blinds, starting_stacks)

# Create a No-Limit Omaha Hold'em game
nlo_game = NLOGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit 5-Card Omaha Hold'em game
flo5_game = FLO5Game(ante, blinds, starting_stacks)

# Create a Pot-Limit 5-Card Omaha Hold'em game
plo5_game = PLO5Game(ante, blinds, starting_stacks)

# Create a No-Limit 5-Card Omaha Hold'em game
nlo5_game = NLO5Game(ante, blinds, starting_stacks)

# Create a Fixed-Limit Greek Hold'em game
flg_game = FLGGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Greek Hold'em game
plg_game = PLGGame(ante, blinds, starting_stacks)

# Create a No-Limit Greek Hold'em game
nlg_game = NLGGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit Short-Deck Hold'em game
fls_game = FLSGame(ante, button_blind, starting_stacks)

# Create a Pot-Limit Short-Deck Hold'em game
pls_game = PLSGame(ante, button_blind, starting_stacks)

# Create a No-Limit Short-Deck Hold'em game
nls_game = NLSGame(ante, button_blind, starting_stacks)

# Create a Kuhn Poker game
kuhn_game = KuhnGame()

# Create a tic tac toe game
ttt_game = TTTGame()

# Create a rock paper scissors game
rps_game = RPSGame()
