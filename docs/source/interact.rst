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

This code outputs the following

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

This code outputs the following

.. code-block:: console

   Pot: 135694700
   Players:
   PokerPlayer(0, 193792375, Ah3sKsKh)
   PokerPlayer(0.00, 0.00)
   Board: 4s5c2h5h9c

The following code demonstrates interacting with No-Limit Short-Deck Hold'em games.

.. literalinclude:: examples/xuan_phua.py
   :language: python

This code outputs the following

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

For more information, you can look at the gameframe API documentations.
