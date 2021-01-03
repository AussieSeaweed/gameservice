.. gameframe documentation master file, created by
   sphinx-quickstart on Sat Dec 26 10:33:27 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GameFrame
=========

GameFrame is a Python game framework library implementing various poker and other board games.

The following games are supported in GameFrame...

- No-Limit Texas Hold'em
- No-Limit Omaha Hold'em
- No-Limit Greek Hold'em
- Tic Tac Toe


Speed
-----

Although, GameFrame is entirely written in Python, it should be fast enough for many tasks.

=================================  ===================
              Game                  Speed (# games/s)
---------------------------------  -------------------
 6-Max No-Limit Texas Hold'em             ~1000
 6-Max No-Limit Omaha Hold'em             ~100
 6-Max No-Limit Greek Hold'em             ~500
 Heads-Up No-Limit Texas Hold'em          ~3000
 Heads-Up No-Limit Omaha Hold'em          ~500
 Heads-Up No-Limit Greek Hold'em          ~2000
 Tic Tac Toe                              ~10000
=================================  ===================

Contributing
------------

Current focuses of development are the following:
   - improve existing games' speed
   - implement more types of games
   - improve documentations

You can contribute on `Github <https://github.com/AussieSeaweed/gameframe>`_.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   install
   create
   interact
   modules


License
-------
`MIT <https://choosealicense.com/licenses/mit/>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
