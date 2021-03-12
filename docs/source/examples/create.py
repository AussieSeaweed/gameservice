from gameframe.poker import (FLBGame, FLCGame, FLFCDGame, FLGGame, FLFCOGame, FLSCOGame, FLOGame, FLSDLB27Game, FLSGame,
                             FLTDLB27Game, FLTGame,
                             KuhnGame,
                             NLBGame, NLCGame, NLFCDGame, NLGGame, NLFCOGame, NLSCOGame, NLOGame, NLSDLB27Game, NLSGame,
                             NLTDLB27Game, NLTGame,
                             PLBGame, PLCGame, PLFCDGame, PLGGame, PLFCOGame, PLSCOGame, PLOGame, PLSDLB27Game, PLSGame,
                             PLTDLB27Game, PLTGame)
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
flfco_game = FLFCOGame(ante, blinds, starting_stacks)

# Create a Pot-Limit 5-Card Omaha Hold'em game
plfco_game = PLFCOGame(ante, blinds, starting_stacks)

# Create a No-Limit 5-Card Omaha Hold'em game
nlfco_game = NLFCOGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit 6-Card Omaha Hold'em game
flsco_game = FLSCOGame(ante, blinds, starting_stacks)

# Create a Pot-Limit 6-Card Omaha Hold'em game
plsco_game = PLSCOGame(ante, blinds, starting_stacks)

# Create a No-Limit 6-Card Omaha Hold'em game
nlsco_game = NLSCOGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit Courchevel game
flc_game = FLCGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Courchevel game
plc_game = PLCGame(ante, blinds, starting_stacks)

# Create a No-Limit Courchevel game
nlc_game = NLCGame(ante, blinds, starting_stacks)

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
flfcd_game = FLFCDGame(ante, blinds, starting_stacks)

# Create a Pot-Limit 5-Card Draw game
plfcd_game = PLFCDGame(ante, blinds, starting_stacks)

# Create a No-Limit 5-Card Draw game
nlfcd_game = NLFCDGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit Badugi game
flb_game = FLBGame(ante, blinds, starting_stacks)

# Create a Pot-Limit Badugi game
plb_game = PLBGame(ante, blinds, starting_stacks)

# Create a No-Limit Badugi game
nlb_game = NLBGame(ante, blinds, starting_stacks)

# Create a Fixed-Limit 2-to-7 Single Draw Lowball game
flsdlb27_game = FLSDLB27Game(ante, blinds, starting_stacks)

# Create a Pot-Limit 2-to-7 Single Draw Lowball game
plsdlb27_game = PLSDLB27Game(ante, blinds, starting_stacks)

# Create a No-Limit 2-to-7 Single Draw Lowball game
nlsdlb27_game = NLSDLB27Game(ante, blinds, starting_stacks)

# Create a Fixed-Limit 2-to-7 Triple Draw Lowball game
fltdlb27_game = FLTDLB27Game(ante, blinds, starting_stacks)

# Create a Pot-Limit 2-to-7 Triple Draw Lowball game
pltdlb27_game = PLTDLB27Game(ante, blinds, starting_stacks)

# Create a No-Limit 2-to-7 Triple Draw Lowball game
nltdlb27_game = NLTDLB27Game(ante, blinds, starting_stacks)

# Create a Kuhn Poker game
kuhn_game = KuhnGame()

# Create a tic tac toe game
ttt_game = TTTGame()

# Create a rock paper scissors game
rps_game = RPSGame()
