GameService
===========

GameService is a Python library that provides a general framework for board games and implements Tic Tac Toe and No
Limit Texas Hold'em Poker games.


Installation
------------

```bash
pip install gameservice
```

Implementation Notes
--------------------

GameService currently implements No Limit Texas Hold'em and Tic Tac Toe games. As it stands right now, you can run ~5000
tic tac toe games per second, and the number of No Limit Texas Hold'em games you can run varies between allowed bet
sizes.


Creating No Limit Texas Hold'em Games
-------------------------------------

To create NLHE games, you first have to define the game parameters, as seen below:

```python
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
        return 0  # Ante


game = TestGame()  # Create a game
```

Creating Tic Tac Toe Games
--------------------------

Tic Tac Toe games are more straight-forward to create.

```python
from gameservice.tictactoe import TicTacToeGame

game = TicTacToeGame()
```

Interacting with Games
----------------------

TicTacToeGame and NLHEGame are subclasses of SequentialGame. The way you interact with instances of
sequential games are the same.

```python
import json

from gameservice.tictactoe import TicTacToeGame

game = TicTacToeGame()

while not game.terminal:
    print(json.dumps(game.player.info_set.serialize(), indent=4))

    actions = game.player.actions

    for action in actions:
        print(action)

    actions[0 if len(actions) == 1 else int(input('Action index: '))].act()

print(json.dumps((game.players[0] if game.nature is None else game.nature).info_set.serialize(), indent=4))
```

Infoset has a serialize method that converts all known info of player to be stored inside a dictionary. Please try out
different games to see the infoset.

License
-------
[MIT](https://choosealicense.com/licenses/mit/)
