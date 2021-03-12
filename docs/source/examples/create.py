from gameframe.poker import (FLBGame, FLD5Game, FLGGame, FLO5Game, FLO6Game, FLOGame, FLSGame, FLTGame, KuhnGame,
                             NLBGame, NLD5Game, NLGGame, NLO5Game, NLO6Game, NLOGame, NLSGame, NLTGame,
                             PLBGame, PLD5Game, PLGGame, PLO5Game, PLO6Game, PLOGame, PLSGame, PLTGame)
from gameframe.rps import RPSGame
from gameframe.ttt import TTTGame

ante = 1
blinds = 1, 2
button_blind = 2
starting_stacks = 200, 200, 300

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

# Create a Fixed-Limit 6-Card Omaha Hold'em game
flo6_game = FLO6Game(ante, blinds, starting_stacks)

# Create a Pot-Limit 6-Card Omaha Hold'em game
plo6_game = PLO6Game(ante, blinds, starting_stacks)

# Create a No-Limit 6-Card Omaha Hold'em game
nlo6_game = NLO6Game(ante, blinds, starting_stacks)

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

# Create a Fixed-Limit 5-Card Draw game
fld5_game = FLD5Game(ante, blinds, starting_stacks)

# Create a Pot-Limit 5-Card Draw game
pld5_game = PLD5Game(ante, blinds, starting_stacks)

# Create a No-Limit 5-Card Draw game
nld5_game = NLD5Game(ante, blinds, starting_stacks)

# Create a Fixed-Limit Badugi game
flb_game = FLBGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Badugi game
plb_game = PLBGame(ante, blinds, starting_stacks)

# Create a No-Limit Badugi game
nlb_game = NLBGame(ante, blinds, starting_stacks)

# Create a Kuhn Poker game
kuhn_game = KuhnGame()

# Create a tic tac toe game
ttt_game = TTTGame()

# Create a rock paper scissors game
rps_game = RPSGame()
