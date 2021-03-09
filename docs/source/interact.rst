Interacting with Games
======================

In order to use the gameframe package in your project, you must first import it.

.. code-block:: python

   from gameframe import ...


Interacting with Poker games
----------------------------

The following code demonstrates interacting with No-Limit Texas Hold'em games.

.. literalinclude:: examples/dwan_ivey.py
   :language: python

This code outputs the following:

.. code-block:: console

   Pot: 1109500
   Players:
   PokerPlayer(0, 572100, Ac2d)
   PokerPlayer(0, 1997500)
   PokerPlayer(0, 1109500, 7h6h)
   Board: Jc3d5c4hJh

The following code demonstrates interacting with Pot-Limit Omaha Hold'em games.

.. literalinclude:: examples/antonius_isildur.py
   :language: python

This code outputs the following:

.. code-block:: console

   Pot: 135694700
   Players:
   PokerPlayer(0, 193792375, Ah3sKsKh)
   PokerPlayer(0.00, 0.00)
   Board: 4s5c2h5h9c

The following code demonstrates interacting with No-Limit Short-Deck Hold'em games.

.. literalinclude:: examples/xuan_phua.py
   :language: python

This code outputs the following:

.. code-block:: console

   Pot: 623000
   Players:
   PokerPlayer(0, 489000)
   PokerPlayer(0, 226000)
   PokerPlayer(0, 684000, QhQd)
   PokerPlayer(0, 400000)
   PokerPlayer(0, 0, KhKs)
   PokerPlayer(0, 198000)
   Board: 9h6cKcJhTs

All poker games can be interacted in an alternative way, using parsers. The following game is equivalent to the game
between Xuan and Phua shown just above.

.. literalinclude:: examples/xuan_phua_parser.py
   :language: python

Of course, this code also prints the exact same output, as shown:

.. code-block:: console

   Pot: 623000
   Players:
   PokerPlayer(0, 489000)
   PokerPlayer(0, 226000)
   PokerPlayer(0, 684000, QhQd)
   PokerPlayer(0, 400000)
   PokerPlayer(0, 0, KhKs)
   PokerPlayer(0, 198000)
   Board: 9h6cKcJhTs


Interacting with Tic Tac Toe games
----------------------------------

I don't expect people to use GameFrame for Tic Tac Toe games, but this section will explain how to play tic tac toe
games.

.. literalinclude:: examples/ttt.py
   :language: python

This code outputs:

.. code-block:: console

   Board:
   X O X
   X O O
   O X O
   Winner: None

You can also use the parser, as demonstrated below:

.. literalinclude:: examples/ttt_parser.py
   :language: python

This code outputs:

.. code-block:: console

   Board:
   O O O
   X X None
   None None None
   Winner: O

Note that each poker player has a string representation of either 'X' or 'O'.


Interacting with Rock Paper Scissors games
------------------------------------------

Rock Paper Scissors game is the simplest game implemented on GameFrame. The following code demonstrates how to use it.

.. literalinclude:: examples/rps.py
   :language: python

This code outputs:

.. code-block:: console

   Hands: RPSHand.ROCK RPSHand.PAPER
   Winner: Second

For more information, you can look at the gameframe API documentations.
