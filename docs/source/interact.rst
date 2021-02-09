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

   Players:
   PokerPlayer(0, 572100, [Ac, 2d])
   PokerPlayer(0, 1997500)
   PokerPlayer(0, 1109500, [7h, 6h])
   Board: Jc 3d 5c 4h Jh

The following code demonstrates interacting with no-limit Omaha Hold'em games.

.. literalinclude:: examples/antonius_isildur.py
   :language: python

This code outputs the following

.. code-block:: console

   Players:
   PokerPlayer(0, 1937923.75, [Ah, 3s, Ks, Kh])
   PokerPlayer(0.00, 0.00)
   Board: 4s 5c 2h 5h 9c

For more information, you can look at the gameframe api documentations.
