Interacting with Games
======================

After creating a game, you can interact with it.

Interacting with Poker games
----------------------------

The following code demonstrates interacting with no-limit Texas Hold'em games.

.. literalinclude:: examples/dwan_ivey.py
   :language: python

This code outputs the following

.. code-block:: console

   Pot: 1109500
   Players:
   PokerPlayer(0, 572100, Ac2d)
   PokerPlayer(0, 1997500)
   PokerPlayer(0, 1109500, 7h6h)
   Board: Jc3d5c4hJh

The following code demonstrates interacting with no-limit Omaha Hold'em games.

.. literalinclude:: examples/antonius_isildur.py
   :language: python

This code outputs the following

.. code-block:: console

   Pot: 135694700
   Players:
   PokerPlayer(0, 193792375, Ah3sKsKh)
   PokerPlayer(0.00, 0.00)
   Board: 4s5c2h5h9c

For more information, you can look at the gameframe api documentations.
