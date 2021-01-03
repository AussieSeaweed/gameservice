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
    nlhe_game = NoLimitTexasHoldEmGame(ante, blinds, starting_stacks, True)

    # Create a no-limit omaha hold'em game
    nlo_game = NoLimitOmahaHoldEmGame(ante, blinds, starting_stacks, True)

    # Create a no-limit greek hold'em game
    nlg_game = NoLimitGreekHoldEmGame(ante, blinds, starting_stacks, True)

    # Create a tic tac toe game
    ttt_game = TicTacToeGame()

The final boolean parameter supplied when creating poker games denote whether or not the poker game is lazy. Lazy poker
games only create the minimum and maximum bet/raise actions when the actor's actions are queried whereas, in non-lazy
poker games, every single possible integer amount bet/raise actions are created.

For most purposes, set lazy to True for vastly improved performance. If you want to make a bet/raise action with amount
in between on a lazy poker game, you can create an AggressiveAction object in gameframe.poker.

