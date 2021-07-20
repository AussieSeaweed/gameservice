Example Games
=============

This section goes over some of the example games defined in the GameFrame package, which are as follows:

- Rock Paper Scissors: :mod:`gameframe.games.rockpaperscissors`
- Tic Tac Toe: :mod:`gameframe.games.tictactoe`

Rock Paper Scissors Games
-------------------------

Rock Paper Scissors game is the simplest game implemented on GameFrame. It is a non-sequential game. The following codes
demonstrates all the attributes, properties, and methods implemented by
:class:`gameframe.games.rockpaperscissors.RockPaperScissorsGame` and
:class:`gameframe.games.rockpaperscissors.RockPaperScissorsPlayer`, which are classes of rock paper scissor games and
rock paper scissors players, respectively.

.. code-block:: python

   from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand

   # Create a three player rock paper scissors game.
   game = RockPaperScissorsGame(3)

   # The winners of the game (None if the game is not yet terminal).
   game.winners
   # The losers of the game (None if the game is not yet terminal).
   game.losers

   # Get the first player.
   player = game.players[0]

   # The hand of the player.
   player.hand

   # Throw a random hand.
   player.throw()
   # Throw the specified hand.
   player.throw(RockPaperScissorsHand.ROCK)
   # True if the player can throw any hand.
   player.can_throw()
   # True if the player can throw the specified hand.
   player.can_throw(RockPaperScissorsHand.SCISSORS)

Rock paper scissors hands are represented by an enum class named
:class:`gameframe.games.rockpaperscissors.RockPaperScissorsHand`. It has the following enum members:

- Rock: :attr:`gameframe.games.rockpaperscissors.RockPaperScissorsHand.ROCK`
- Paper: :attr:`gameframe.games.rockpaperscissors.RockPaperScissorsHand.PAPER`
- Scissors: :attr:`gameframe.games.rockpaperscissors.RockPaperScissorsHand.SCISSORS`

The following code demonstrates interacting with rock paper scissor games.

.. code-block:: python

   from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand

   game = RockPaperScissorsGame()

   game.players[0].throw(RockPaperScissorsHand.ROCK)
   game.players[1].throw(RockPaperScissorsHand.PAPER)

   print(next(game.winners).index)  # 1 (The second player)

Note that the attribute :attr:`gameframe.games.rockpaperscissors.RockPaperScissorsGame.winners` is named with a plural
symbol, as, when there are more than 3 players, the game might have multiple winners. When there are no winners, the
property returns an empty iterator.

Here, nothing is passed to the constructor to the :class:`gameframe.games.rockpaperscissors.RockPaperScissorsGame`. In
this case, the number of players are assumed to be 2.

Tic Tac Toe Games
-----------------

This section will explain how to play tic tac toe games.

Below shows all possible member variables, properties, and methods of the related classes
:class:`gameframe.games.tictactoe.TicTacToeGame` and :class:`gameframe.games.tictactoe.TicTacToePlayer`.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   # Create a tic tac toe game.
   game = TicTacToeGame()

   # The board of the game.
   game.board
   # A sequence of empty coordinates of the game.
   game.empty_coordinates
   # The winner of the game (either None or one of the players).
   game.winner

   # Get the first player.
   player = game.players[0]

   # Mark a random empty coordinate.
   player.mark()
   # Mark the coordinate.
   player.mark(1, 1)
   # True if the player can mark any coordinate.
   player.can_mark()
   # True if the player can mark the corresponding coordinate.
   player.can_mark(0, 0)

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

   print(game.winner)  # None (A tied game)

By the end of the game, the board looks like the following:

.. code-block:: console

   X   O   X
   X   O   O
   O   X   O

A simpler way of interacting with tic tac toe exists, which uses :meth:`gameframe.games.tictactoe.TicTacToeGame.mark`.

.. code-block:: python

   from gameframe.games.tictactoe import TicTacToeGame

   game = TicTacToeGame()

   game.mark((0, 0), (1, 0), (0, 1), (1, 1), (0, 2))

   print(game.winner.index)  # 0 (The first player)

The game result is as follows:

.. code-block:: console

   O   O   O
   X   X   .
   .   .   .

Note that the winner in the above game scenario is the first player.

More Information
----------------

For more information, you can look at the gameframe API documentations.
