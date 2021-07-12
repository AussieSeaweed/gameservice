Game Interactions
=================

In order to use the gameframe package in your project, you must first import it.

.. code-block:: python

   from gameframe import *

Interacting with Games
----------------------

All games implemented in gameframe share some attributes.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   # Create a game.
   game = TicTacToeGame()

   # Get the nature.
   game.nature
   # Get the players.
   game.players
   # True if the game is terminal, else False.
   game.is_terminal()

   actor = game.nature

   # The game of this actor.
   actor.game
   # None if this actor is the nature, else the index of this player.
   actor.index
   # True if the actor is the nature, else False.
   actor.is_nature()
   # True if the actor is one of the players, else False.
   actor.is_player()

Currently, all implemented games have natures that are irrelevant to the gameplay. However, in some games, such as
poker, natures play a crucial role.

Interacting with Sequential Games
---------------------------------

Sequential games have an extra actor attribute that can be accessed. It represents the current player to act.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   # Create a sequential game.
   game = TicTacToeGame()

   # Get the current actor (either None, the nature or one of the players).
   game.actor

   actor = game.players[0]

   # True if this actor is in turn to act, else False.
   actor.is_actor()

Interacting with Rock Paper Scissors Games
------------------------------------------

Rock Paper Scissors game is the simplest game implemented on GameFrame. The following codes demonstrates how to use it.

.. code-block:: python

   from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand

   game = RockPaperScissorsGame()
   player = game.players[0]

   # Throw a random hand.
   player.throw()
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

.. code-block:: python

   from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand

   game = RockPaperScissorsGame()
   x, y = game.players

   x.throw(RockPaperScissorsHand.ROCK)
   y.throw(RockPaperScissorsHand.PAPER)

This code results in the following:

.. code-block:: console

   Hands: RockPaperScissorsHand.ROCK RockPaperScissorsHand.PAPER
   Winner: Second

Interacting with Tic Tac Toe Games
----------------------------------

This section will explain how to play tic tac toe games.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   game = TicTacToeGame()

   player = game.players[0]

   # Mark a random empty coordinate.
   player.mark()
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

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   game = TicTacToeGame()
   x, y = game.players

   x.mark(1, 1)
   y.mark(0, 0)
   x.mark(2, 0)
   y.mark(0, 2)
   x.mark(0, 1)
   y.mark(2, 1)
   x.mark(1, 2)
   y.mark(1, 0)
   x.mark(2, 2)

The game result is as follows:

.. code-block:: console

   Board:
   X O X
   X O O
   O X O
   Winner: None

You can simplify this, as demonstrated below:

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   game = TicTacToeGame()

   game.mark((0, 0), (1, 0), (0, 1), (1, 1), (0, 2))

The game result is as follows:

.. code-block:: console

   Board:
   O    O    O
   X    X    None
   None None None
   Winner: O

Note that each poker player has a string representation of either 'X' or 'O'.

For more information, you can look at the gameframe API documentations.
