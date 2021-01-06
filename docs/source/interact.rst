Interacting with Games
======================

After creating a game, you can interact with it.

Interacting with Sequential Games
---------------------------------

All poker games and tic tac toe games are subclasses of SequentialGame, meaning they are sequential games. The way you interact with every instance of
sequential games are the same.

The most general way of interacting with sequential games are as follows:

.. code-block:: python

    from gameframe.tictactoe import TicTacToeGame
    from gameframe.utils import pretty_print

    game = TicTacToeGame()  # Create a tic tac toe game

    # Interact with the game.

    while not game.terminal:
        pretty_print(game.actor.information_set)  # Print the current actor's information set

        game.actor.actions[int(input('Action #: '))].act()

    # Print final game state.

    pretty_print(game.nature.information_set)

Try out the following code to get a sense of how things work in GameFrame.

You can notice that all game information is shown in the information_set dictionary. Obviously, obtaining information
this way is not ideal. Thus, you can also access individual game elements as follows:

.. code-block:: python

    from gameframe.poker import NoLimitTexasHoldEmGame
    from gameframe.tictactoe import TicTacToeGame

    # Create a NLHE game
    nlhe_game = NoLimitTexasHoldEmGame(1, [1, 2], [200, 300, 200], True)

    print(nlhe_game.actor)  # Print the current actor (might be nature or one of the players)
    print(nlhe_game.actor.nature)  # True if the actor is nature, otherwise False
    print(nlhe_game.nature)  # Print the nature
    print(nlhe_game.players)  # Print the list of players

    print(nlhe_game.players[0].bet)  # Print the bet of the first player
    print(nlhe_game.players[0].stack)  # Print the stack of the first player
    print(nlhe_game.players[0].hole_cards)  # Print the hole cards of the first player

    print(nlhe_game.environment.pot)  # Print the pot
    print(nlhe_game.environment.board_cards)  # Print the board

    ...

    nlhe_game.nature.progress()  # Set up next street

    ...

    nlhe_game.players[2].fold()  # Fold
    nlhe_game.players[0].bet_raise(6)  # Raise
    nlhe_game.players[1].check_call()  # Call

    ...

    print(nlhe_game.players[0].payoff)  # Print the result of the player (+gain or -loss)

    ...

    # Create a tic tac toe game
    ttt_game = TicTacToeGame()

    ...

    print(ttt_game.environment.board)  # Print the board

    ...

    ttt_game.players[0].mark(0, 0)  # Mark coordinate (0, 0)

    ...

    print(ttt_game.players[0].payoff)  # 1 if the player won, -1 if the player lost, 0 if tied

For more information, you can look at the game api documentations.
