Interacting with Games
======================

In order to use the gameframe package in your project, you must first import it.

.. code-block:: python

   from gameframe import ...


All games implemented in gameframe share some attributes.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   # Create a no-limit Texas Hold'em game.
   game = TicTacToeGame()

   # Get the nature.
   game.nature
   # Get the players.
   game.players
   # True if the game is terminal, else False.
   game.is_terminal()


Currently, all implemented games have natures that are irrelevant to the gameplay. However, in some games, such as
poker, natures play a crucial role.


Interacting with Sequential games
---------------------------------

Almost all games (currently except rock paper scissors) are sequential games. They have an extra actor attribute that
can be accessed. It represents the current player to act.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   # Create a no-limit Texas Hold'em game.
   game = TicTacToeGame()

   # Get the current actor (either None, the nature or one of the players).
   game.actor


Interacting with Tic Tac Toe games
----------------------------------

This section will explain how to play tic tac toe games.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   game = TicTacToeGame()

   player = game.players[0]

   # Mark the coordinate.
   player.mark(1, 1)
   # True if the player can mark any coordinate.
   player.can_mark()
   # True if the player can mark the corresponding coordinate.
   player.can_mark(0, 0)

   # The board of the game.
   game.board
   # A sequence of empty coordinates of the game.
   game.empty_coordinates
   # The winner of the game (either None or one of the players).
   game.winner


The code below demonstrates a sample tic tac toe game.

.. literalinclude:: examples/tictactoe.py
   :language: python

The game result is as follows:

.. code-block:: console

   Board:
   X O X
   X O O
   O X O
   Winner: None


You can also use the parser, as demonstrated below:

.. literalinclude:: examples/tictactoe_parser.py
   :language: python


The game result is as follows:

.. code-block:: console

   Board:
   O    O    O
   X    X    None
   None None None
   Winner: O


Note that each poker player has a string representation of either 'X' or 'O'.


Interacting with Rock Paper Scissors games
------------------------------------------

Rock Paper Scissors game is the simplest game implemented on GameFrame. The following codes demonstrates how to use it.

.. code-block:: python

   from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand

   game = RockPaperScissorsGame()
   player = game.players[0]

   # Throw the specified hand.
   player.throw(RockPaperScissorsHand.ROCK)
   # True if the player can throw any hand.
   player.can_throw()
   # True if the player can throw the specified hand.
   player.can_throw(RockPaperScissorsHand.SCISSORS)

   # The winner of the game (either None or one of the players).
   game.winner
   # The hand of the player.
   player.hand


This is a sample game.

.. literalinclude:: examples/rockpaperscissors.py
   :language: python


This code results in the following:

.. code-block:: console

   Hands: RockPaperScissorsHand.ROCK RockPaperScissorsHand.PAPER
   Winner: Second


For more information, you can look at the gameframe API documentations.
