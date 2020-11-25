GameService
===========

A library that implements various board games 
and provide a general framework for various board games.


Installation
------------

```bash
pip install gameservice
```


Implementation Notes
--------------------

GameService currently implements No Limit Texas Hold'em and Tic Tac Toe games. 
As it stands right now, you can run ~5000 tic tac toe games per second, and 
~100 games per second of 9-Max NLHE with maximum of 20 bet sizes if players take random actions.
As for NLHE games, since most of the actions will be folds, calls, checks, or 
raises with predictible bet sizes, real life performance for them will be vastly
better if NLHELazyGame class is used.


Creating No Limit Texas Hold'em Games
-------------------------------------

You first have to define the game parameters


```python
from gameservice.poker import NLHELazyGame


class TestGame(NLHELazyGame):
    @property
    def starting_stacks(self):
        return [200, 400, 300]

    @property
    def blinds(self):
        return [1, 2]

    @property
    def ante(self):
        return 0


game = TestGame()
```

Here, you can define starting stacks, blinds, and ante. Then, you can create 
the game instance as shown.


Creating Tic Tac Toe Games
--------------------------

Tic Tac Toe games are straight-forward to create.


```python
from gameservice.tictactoe import TTTGame

game = TTTGame()
```


Interacting with Games
----------------------

Interacting with every game is basically the same across all games. 
As an example, Tic Tac Toe Game will be used

```python
from gameservice.tictactoe import TTTGame

game = TTTGame()

while not game.terminal:  # Run while the game is not finished
    print(game.player.info_set)  # Get the infoset of player to act

    actions = game.player.actions  # Get the list of possible actions

    for action in actions:
        print(action)  # Each action instance's name will be printed

    actions[int(input('Action index: '))].act()  # Choose an action and act (modify the game)

print('Done!') 
```

Infoset has a serialize method that converts all known info of player to be
stored inside a dictionary. Please try out different games to see the infoset.

License
-------
[MIT](https://choosealicense.com/licenses/mit/)
