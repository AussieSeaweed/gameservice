.. gameframe documentation master file, created by
   sphinx-quickstart on Sat Dec 26 10:33:27 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

gameframe
=========

gameframe is a Python library that provides a general framework for board games and implements poker and tic tac toe
games. Currently, for poker games, only no-limit texas hold'em games are supported.


Installation
------------

gameframe can be installed by typing the following in terminal

.. code-block:: console

   pip install gameframe


Implementation Notes
--------------------

gameframe currently implements No Limit Texas Hold'em and Tic Tac Toe games. As it stands right now, you can run ~5000
tic tac toe games per second. For poker games, the number of games you can run varies depending on the number of bet
sizes, but, for LazyNLHEGame instances (only fold, check, call, min or max bet/raise), ~400 games can be run per second
with randomly chosen actions.

Contributing
------------

Current focuses of development is the following:
   - addint type hints
   - improve existing games' speed
   - implement more types of games
   - improve documentations

You can contribute on `Github <https://github.com/AussieSeaweed/gameframe>`_.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   create
   interact
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
