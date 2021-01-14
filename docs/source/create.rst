Creating Games
==============

Creating games are very simple.

.. code-block:: python

    from gameframe.poker import NoLimitTexasHoldEmGame, NoLimitOmahaHoldEmGame, NoLimitGreekHoldEmGame
    from gameframe.tictactoe import TicTacToeGame

    ante = 1
    blinds = [1, 2]
    starting_stacks = [200, 200, 300]

    # Create a no-limit texas hold'em game
    nlhe_game = NoLimitTexasHoldEmGame(ante, blinds, starting_stacks)

    # Create a no-limit greek hold'em game
    nlg_game = NoLimitGreekHoldEmGame(ante, blinds, starting_stacks)

    # Create a no-limit omaha hold'em game
    nlo_game = NoLimitOmahaHoldEmGame(ante, blinds, starting_stacks)

    # Create a tic tac toe game
    ttt_game = TicTacToeGame()
