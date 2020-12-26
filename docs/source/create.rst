Create Games
============

You can create No-Limit Hold'em and Tic Tac Toe Games with gameservice.


Creating No-Limit Texas Hold'em Games
-------------------------------------

To create NLHE games, you first have to define the game parameters, as seen below:

.. code-block:: python

    from gameservice.poker import NLHEGame


    class TestGame(NLHEGame):
        @property
        def starting_stacks(self):
            return [200, 400, 300]  # Starting stacks also describe the number of players

        @property
        def blinds(self):
            return [1, 2]  # Small blind and big blind.

        @property
        def ante(self):
            return 1  # Ante


    game = TestGame()  # Create a game


You can create lazy no-limit hold'em games by replacing NLHEGame with LazyNLHEGame. The difference between NLHEGame and
LazyNLHEGame is explained in :doc:`gameservice.poker`.


Creating Tic Tac Toe Games
--------------------------

Tic Tac Toe games are more straight-forward to create.

.. code-block:: python

    from gameservice.tictactoe import TicTacToeGame

    game = TicTacToeGame()
