.. gameservice documentation master file, created by
   sphinx-quickstart on Fri Dec 18 17:53:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

gameservice
===========

gameservice is a Python library that provides a general framework for board games and implements poker and tic tac toe
games. Currently, for poker games, only no-limit texas hold'em games are supported.


Installation
------------

gameservice can be installed by typing the following in terminal

.. code-block:: console

   pip install gameservice


Implementation Notes
--------------------

GameService currently implements No Limit Texas Hold'em and Tic Tac Toe games. As it stands right now, you can run ~5000
tic tac toe games per second. For poker games, the number of games you can run varies depending on the number of bet
sizes, but, for LazyNLHEGame instances (only fold, check, call, min or max bet/raise), around 100 games can be run per
second with randomly chosen actions.

Contributing
------------

Current focus of development is to improve existing games' speed and implement more types of games. You can contribute
on `Github <https://github.com/AussieSeaweed/gameservice>`_.

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
