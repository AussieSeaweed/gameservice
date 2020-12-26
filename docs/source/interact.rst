Interact with Games
===================

After creating a game, you can interact with it.

Interacting with Sequential Games
---------------------------------

TicTacToeGame, NLHEGame, and LazyNLHEGame are subclasses of SequentialGame. The way you interact with every instance of
sequential games are the same.

Try out the following code:

.. code-block:: python

    import json

    from gameservice.tictactoe import TicTacToeGame

    game = TicTacToeGame() # Create a tic tac toe game (any sequential game would work)

    while not game.terminal:  # While the game is not over
        print(dumps(game.player.info_set.serialize(), indent=4))  # Pretty print the info-set of the current player

        actions = game.player.actions  # Get the actions of the acting player

        for i, action in enumerate(actions):
            print(f'{i}: {action}')  # Print the actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()  # Choose an action and act

    # Pretty print the info-set of the nature or, if nature does not exist, any player.
    print(dumps((game.players[0] if game.nature is None else game.nature).info_set.serialize(), indent=4))

Here, the dumps function from json is used only to print the dictionary returned by the serialize method in a pretty
manner. Tic tac toe games do not have nature, so I had to create an extra condition at the end to check for nature's
existence.

Example Interaction with LazyNLHEGame
-------------------------------------

This is an example code of interacting with lazy no-limit hold'em games.

.. code-block:: python

    from gameservice.poker import LazyNLHEGame
    import json

    class CustomNLHEGame(LazyNLHEGame):
        @property
        def ante(self):
            return 1

        @property
        def blinds(self):
            return [1, 2]

        @property
        def starting_stacks(self):
            return [200, 100, 50]

    game = CustomNLHEGame()

    while not game.terminal:
        print(dumps(game.player.info_set.serialize(), indent=4))

        actions = game.player.actions

        for i, action in enumerate(actions):
            print(f'{i}: {action}')

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    print(dumps((game.players[0] if game.nature is None else game.nature).info_set.serialize(), indent=4))


The following is an example console interaction (it is very long). In an actual application, you wouldn't interact with
the game this way anyway.

.. code-block:: console

    {
        "environment": {
            "aggressor": null,
            "min_delta": null,
            "pot": 3,
            "board": []
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 6,
            "actions": [
                "Deal 2 hole cards and 0 board cards"
            ],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -2,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 198,
                "bet": 1,
                "hole_cards": [],
                "mucked": false,
                "commitment": 2,
                "total": 199,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 97,
                "bet": 2,
                "hole_cards": [],
                "mucked": false,
                "commitment": 3,
                "total": 99,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -1,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 49,
                "bet": 0,
                "hole_cards": [],
                "mucked": false,
                "commitment": 1,
                "total": 49,
                "effective_stack": 49,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 2 hole cards and 0 board cards
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": 2,
            "pot": 3,
            "board": []
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 6,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -2,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 198,
                "bet": 1,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 2,
                "total": 199,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [],
                "next": "Nature",
                "str": "Player 1",
                "stack": 97,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 3,
                "total": 99,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -1,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 49",
                    "Raise 4"
                ],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 49,
                "bet": 0,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 1,
                "total": 49,
                "effective_stack": 49,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Fold
    1: Call 2
    2: Raise 49
    3: Raise 4
    Action #: 3
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": 2,
            "pot": 3,
            "board": []
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 10,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -2,
                "actions": [
                    "Fold",
                    "Call 3",
                    "Raise 6",
                    "Raise 199"
                ],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 198,
                "bet": 1,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 2,
                "total": 199,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [],
                "next": "Nature",
                "str": "Player 1",
                "stack": 97,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 3,
                "total": 99,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 45,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 5,
                "total": 49,
                "effective_stack": 49,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Fold
    1: Call 3
    2: Raise 6
    3: Raise 199
    Action #: 2
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 3,
            "board": []
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 15,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 6,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 199,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [
                    "Fold",
                    "Call 4",
                    "Raise 8",
                    "Raise 99"
                ],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 97,
                "bet": 2,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": 3,
                "total": 99,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 45,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 5,
                "total": 49,
                "effective_stack": 49,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Fold
    1: Call 4
    2: Raise 8
    3: Raise 99
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 3,
            "board": []
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 19,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 6,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 199,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 6,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 99,
                "effective_stack": 99,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 8",
                    "Raise 49"
                ],
                "next": "Nature",
                "str": "Player 2",
                "stack": 45,
                "bet": 4,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 5,
                "total": 49,
                "effective_stack": 49,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Fold
    1: Call 2
    2: Raise 8
    3: Raise 49
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": null,
            "pot": 21,
            "board": []
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [
                "Deal 0 hole cards and 3 board cards"
            ],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 0 hole cards and 3 board cards
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [
                    "Check",
                    "Bet 193",
                    "Bet 2"
                ],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": "5274 (Pair)"
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Check
    1: Bet 193
    2: Bet 2
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 93"
                ],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": "7155 (High Card)"
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Check
    1: Bet 2
    2: Bet 93
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 43"
                ],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": "6295 (High Card)"
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Check
    1: Bet 2
    2: Bet 43
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": null,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [
                "Deal 0 hole cards and 1 board cards"
            ],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 0 hole cards and 1 board cards
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [
                    "Check",
                    "Bet 193",
                    "Bet 2"
                ],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": "3111 (Two Pair)"
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Check
    1: Bet 193
    2: Bet 2
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 93"
                ],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": "4762 (Pair)"
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Check
    1: Bet 2
    2: Bet 93
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 43"
                ],
                "next": "Nature",
                "str": "Player 2",
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": "4649 (Pair)"
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Check
    1: Bet 2
    2: Bet 43
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 23,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 193",
                    "Raise 4"
                ],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": "3111 (Two Pair)"
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "next": "Nature",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -9,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 41,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 9,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Fold
    1: Call 2
    2: Raise 193
    3: Raise 4
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 25,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 191,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 9,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 4",
                    "Raise 93"
                ],
                "next": "Nature",
                "str": "Player 1",
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": 7,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": "4762 (Pair)"
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -9,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 41,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 9,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Fold
    1: Call 2
    2: Raise 4
    3: Raise 93
    Action #: 2
    {
        "environment": {
            "aggressor": "Player 1",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 29,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [],
                "next": "Nature",
                "str": "Player 0",
                "stack": 191,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 9,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 89,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -9,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 43",
                    "Raise 6"
                ],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 41,
                "bet": 2,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 9,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": "4649 (Pair)"
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Fold
    1: Call 2
    2: Raise 43
    3: Raise 6
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 1",
            "min_delta": 2,
            "pot": 21,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 31,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 193",
                    "Raise 6"
                ],
                "next": "Nature",
                "str": "Player 0",
                "stack": 191,
                "bet": 2,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 9,
                "total": 193,
                "effective_stack": 93,
                "relevant": true,
                "hand": "3111 (Two Pair)"
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 89,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 93,
                "effective_stack": 93,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -11,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 39,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 43,
                "effective_stack": 43,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Fold
    1: Call 2
    2: Raise 193
    3: Raise 6
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 1",
            "min_delta": null,
            "pot": 33,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 33,
            "actions": [
                "Deal 0 hole cards and 1 board cards"
            ],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [],
                "next": "Nature",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 189,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 89,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 89,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -11,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 39,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 39,
                "effective_stack": 39,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 0 hole cards and 1 board cards
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 33,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 33,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 189"
                ],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 11,
                "total": 189,
                "effective_stack": 89,
                "relevant": true,
                "hand": "3111 (Two Pair)"
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 89,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 89,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -11,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 39,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 39,
                "effective_stack": 39,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Check
    1: Bet 2
    2: Bet 189
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 33,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 33,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 189,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [
                    "Check",
                    "Bet 89",
                    "Bet 2"
                ],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 89,
                "bet": 0,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": 11,
                "total": 89,
                "effective_stack": 89,
                "relevant": true,
                "hand": "3152 (Two Pair)"
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -11,
                "actions": [],
                "next": "Nature",
                "str": "Player 2",
                "stack": 39,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 39,
                "effective_stack": 39,
                "relevant": true,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Check
    1: Bet 89
    2: Bet 2
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 0",
            "min_delta": 2,
            "pot": 33,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 33,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 189,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [],
                "next": "Player 2",
                "str": "Player 1",
                "stack": 89,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 89,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -11,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 39"
                ],
                "next": "Nature",
                "str": "Player 2",
                "stack": 39,
                "bet": 0,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 11,
                "total": 39,
                "effective_stack": 39,
                "relevant": true,
                "hand": "4649 (Pair)"
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Check
    1: Bet 2
    2: Bet 39
    Action #: 2
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": 39,
            "pot": 33,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 72,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [
                    "Fold",
                    "Call 39",
                    "Raise 189",
                    "Raise 78"
                ],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": [
                    "3s",
                    "6d"
                ],
                "mucked": false,
                "commitment": 11,
                "total": 189,
                "effective_stack": 89,
                "relevant": true,
                "hand": "3111 (Two Pair)"
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [],
                "next": "Nature",
                "str": "Player 1",
                "stack": 89,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 11,
                "total": 89,
                "effective_stack": 89,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "next": "Player 0",
                "str": "Player 2",
                "stack": 0,
                "bet": 39,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 50,
                "total": 39,
                "effective_stack": 39,
                "relevant": false,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 39"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Fold
    1: Call 39
    2: Raise 189
    3: Raise 78
    Action #: 0
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": 39,
            "pot": 33,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 72,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": null,
                "mucked": true,
                "commitment": 11,
                "total": 189,
                "effective_stack": 89,
                "relevant": false,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -11,
                "actions": [
                    "Fold",
                    "Call 39"
                ],
                "next": "Nature",
                "str": "Player 1",
                "stack": 89,
                "bet": 0,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": 11,
                "total": 89,
                "effective_stack": 89,
                "relevant": true,
                "hand": "3152 (Two Pair)"
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "next": "Player 1",
                "str": "Player 2",
                "stack": 0,
                "bet": 39,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 50,
                "total": 39,
                "effective_stack": 39,
                "relevant": false,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 39",
            "Player 0: Fold"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Fold
    1: Call 39
    Action #: 1
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": null,
            "pot": 111,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 111,
            "actions": [
                "Showdown"
            ],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": null,
                "mucked": true,
                "commitment": 11,
                "total": 189,
                "effective_stack": 50,
                "relevant": false,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -50,
                "actions": [],
                "next": "Nature",
                "str": "Player 1",
                "stack": 50,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 50,
                "total": 50,
                "effective_stack": 50,
                "relevant": true,
                "hand": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "next": "Player 1",
                "str": "Player 2",
                "stack": 0,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ],
                "mucked": false,
                "commitment": 50,
                "total": 0,
                "effective_stack": 0,
                "relevant": false,
                "hand": null
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 39",
            "Player 0: Fold",
            "Player 1: Call 39"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Showdown
    {
        "environment": {
            "aggressor": "Player 2",
            "min_delta": null,
            "pot": 0,
            "board": [
                "8d",
                "9c",
                "6h",
                "8s",
                "2c"
            ]
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 0,
            "actions": [],
            "next": "Nature",
            "str": "Nature"
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -11,
                "actions": [],
                "next": "Player 1",
                "str": "Player 0",
                "stack": 189,
                "bet": 0,
                "hole_cards": null,
                "mucked": true,
                "commitment": 11,
                "total": 189,
                "effective_stack": 161,
                "relevant": false,
                "hand": null
            },
            {
                "nature": false,
                "index": 1,
                "payoff": 61,
                "actions": [],
                "next": "Nature",
                "str": "Player 1",
                "stack": 161,
                "bet": 0,
                "hole_cards": [
                    "Qd",
                    "2s"
                ],
                "mucked": false,
                "commitment": -61,
                "total": 161,
                "effective_stack": 161,
                "relevant": true,
                "hand": "3152 (Two Pair)"
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "next": "Player 1",
                "str": "Player 2",
                "stack": 0,
                "bet": 0,
                "hole_cards": [
                    "Ah",
                    "Kc"
                ],
                "mucked": false,
                "commitment": 50,
                "total": 0,
                "effective_stack": 0,
                "relevant": false,
                "hand": "4649 (Pair)"
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Raise 6",
            "Player 1: Call 4",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Check",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Raise 4",
            "Player 2: Call 2",
            "Player 0: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 39",
            "Player 0: Fold",
            "Player 1: Call 39",
            "Nature: Showdown"
        ],
        "terminal": true,
        "player": null
    }
