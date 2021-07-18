.. gameframe documentation master file, created by
   sphinx-quickstart on Sat Dec 26 10:33:27 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GameFrame
=========

GameFrame is a Python package for a general game framework.

It provides base classes for implementing simple games. In addition, some example games are already implemented in
GameFrame...

- Tic Tac Toe
- Rock Paper Scissors

Many poker game variants are also implemented on the `PokerTools <https://pokertools.readthedocs.io/>`_ package.

Speed
-----

Although GameFrame is entirely written in Python, it should be fast enough for many tasks.

=================================  ===================
              Game                  Speed (# games/s)
---------------------------------  -------------------
 Tic Tac Toe                              ~10000
 Rock Paper Scissors                      ~100000
=================================  ===================

Contributing
------------

Current focuses of development are the following:

   - improve existing games' speed
   - implement more types of games
   - improve documentations

You can contribute on `Github <https://github.com/AussieSeaweed/gameframe>`_.

License
-------

`GNU GPLv3 <https://choosealicense.com/licenses/gpl-3.0/>`_

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   setup
   bases
   examples
   gameframe

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
