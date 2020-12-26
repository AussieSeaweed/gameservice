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
            "min_delta": null,
            "pot": 3,
            "board": [],
            "aggressor": null
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 6,
            "actions": [
                "Deal 2 hole cards and 0 board cards"
            ]
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -2,
                "actions": [],
                "stack": 198,
                "bet": 1,
                "hole_cards": []
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [],
                "stack": 97,
                "bet": 2,
                "hole_cards": []
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -1,
                "actions": [],
                "stack": 49,
                "bet": 0,
                "hole_cards": []
            }
        ],
        "logs": [],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 2 hole cards and 0 board cards
    {
        "environment": {
            "min_delta": 2,
            "pot": 3,
            "board": [],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 6,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -2,
                "actions": [],
                "stack": 198,
                "bet": 1,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [],
                "stack": 97,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
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
                "stack": 49,
                "bet": 0,
                "hole_cards": [
                    "7s",
                    "3c"
                ]
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
            "min_delta": 2,
            "pot": 3,
            "board": [],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 10,
            "actions": []
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
                "stack": 198,
                "bet": 1,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [],
                "stack": 97,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "stack": 45,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ]
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
    Action #: 1
    {
        "environment": {
            "min_delta": 2,
            "pot": 3,
            "board": [],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 13,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -5,
                "actions": [],
                "stack": 195,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -3,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 99",
                    "Raise 6"
                ],
                "stack": 97,
                "bet": 2,
                "hole_cards": [
                    "As",
                    "Ks"
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "stack": 45,
                "bet": 4,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Fold
    1: Call 2
    2: Raise 99
    3: Raise 6
    Action #: 1
    {
        "environment": {
            "min_delta": null,
            "pot": 15,
            "board": [],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 15,
            "actions": [
                "Deal 0 hole cards and 3 board cards"
            ]
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -5,
                "actions": [],
                "stack": 195,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -5,
                "actions": [],
                "stack": 95,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "stack": 45,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 0 hole cards and 3 board cards
    {
        "environment": {
            "min_delta": 2,
            "pot": 15,
            "board": [
                "3d",
                "9h",
                "5h"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 15,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -5,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 195"
                ],
                "stack": 195,
                "bet": 0,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -5,
                "actions": [],
                "stack": 95,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "stack": 45,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Check
    1: Bet 2
    2: Bet 195
    Action #: 0
    {
        "environment": {
            "min_delta": 2,
            "pot": 15,
            "board": [
                "3d",
                "9h",
                "5h"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 15,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -5,
                "actions": [],
                "stack": 195,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -5,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 95"
                ],
                "stack": 95,
                "bet": 0,
                "hole_cards": [
                    "As",
                    "Ks"
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [],
                "stack": 45,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Check
    1: Bet 2
    2: Bet 95
    Action #: 0
    {
        "environment": {
            "min_delta": 2,
            "pot": 15,
            "board": [
                "3d",
                "9h",
                "5h"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 15,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -5,
                "actions": [],
                "stack": 195,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -5,
                "actions": [],
                "stack": 95,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -5,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 45"
                ],
                "stack": 45,
                "bet": 0,
                "hole_cards": [
                    "7s",
                    "3c"
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Check
    1: Bet 2
    2: Bet 45
    Action #: 1
    {
        "environment": {
            "min_delta": 2,
            "pot": 15,
            "board": [
                "3d",
                "9h",
                "5h"
            ],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 17,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -5,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 195",
                    "Raise 4"
                ],
                "stack": 195,
                "bet": 0,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -5,
                "actions": [],
                "stack": 95,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "stack": 43,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Fold
    1: Call 2
    2: Raise 195
    3: Raise 4
    Action #: 1
    {
        "environment": {
            "min_delta": 2,
            "pot": 15,
            "board": [
                "3d",
                "9h",
                "5h"
            ],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 19,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "stack": 193,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -5,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 4",
                    "Raise 95"
                ],
                "stack": 95,
                "bet": 0,
                "hole_cards": [
                    "As",
                    "Ks"
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "stack": 43,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
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
    3: Raise 95
    Action #: 1
    {
        "environment": {
            "min_delta": null,
            "pot": 21,
            "board": [
                "3d",
                "9h",
                "5h"
            ],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": [
                "Deal 0 hole cards and 1 board cards"
            ]
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -7,
                "actions": [],
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 0 hole cards and 1 board cards
    {
        "environment": {
            "min_delta": 2,
            "pot": 21,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 21,
            "actions": []
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
                "stack": 193,
                "bet": 0,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Check
    1: Bet 193
    2: Bet 2
    Action #: 2
    {
        "environment": {
            "min_delta": 2,
            "pot": 21,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 23,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [],
                "stack": 191,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
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
                "stack": 93,
                "bet": 0,
                "hole_cards": [
                    "As",
                    "Ks"
                ]
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [],
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2"
        ],
        "terminal": false,
        "player": "Player 1"
    }
    0: Fold
    1: Call 2
    2: Raise 4
    3: Raise 93
    Action #: 0
    {
        "environment": {
            "min_delta": 2,
            "pot": 21,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 23,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [],
                "stack": 191,
                "bet": 2,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -7,
                "actions": [
                    "Fold",
                    "Call 2",
                    "Raise 43",
                    "Raise 4"
                ],
                "stack": 43,
                "bet": 0,
                "hole_cards": [
                    "7s",
                    "3c"
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Fold
    1: Call 2
    2: Raise 43
    3: Raise 4
    Action #: 1
    {
        "environment": {
            "min_delta": null,
            "pot": 25,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 25,
            "actions": [
                "Deal 0 hole cards and 1 board cards"
            ]
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [],
                "stack": 191,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -9,
                "actions": [],
                "stack": 41,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold",
            "Player 2: Call 2"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Deal 0 hole cards and 1 board cards
    {
        "environment": {
            "min_delta": 2,
            "pot": 25,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh",
                "8d"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 25,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [
                    "Check",
                    "Bet 2",
                    "Bet 191"
                ],
                "stack": 191,
                "bet": 0,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -9,
                "actions": [],
                "stack": 41,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Check
    1: Bet 2
    2: Bet 191
    Action #: 0
    {
        "environment": {
            "min_delta": 2,
            "pot": 25,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh",
                "8d"
            ],
            "aggressor": "Player 0"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 25,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [],
                "stack": 191,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -9,
                "actions": [
                    "Check",
                    "Bet 41",
                    "Bet 2"
                ],
                "stack": 41,
                "bet": 0,
                "hole_cards": [
                    "7s",
                    "3c"
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check"
        ],
        "terminal": false,
        "player": "Player 2"
    }
    0: Check
    1: Bet 41
    2: Bet 2
    Action #: 1
    {
        "environment": {
            "min_delta": 41,
            "pot": 25,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh",
                "8d"
            ],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 66,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -9,
                "actions": [
                    "Fold",
                    "Call 41"
                ],
                "stack": 191,
                "bet": 0,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "stack": 0,
                "bet": 41,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 2: Bet 41"
        ],
        "terminal": false,
        "player": "Player 0"
    }
    0: Fold
    1: Call 41
    Action #: 1
    {
        "environment": {
            "min_delta": null,
            "pot": 107,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh",
                "8d"
            ],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 107,
            "actions": [
                "Showdown"
            ]
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": -50,
                "actions": [],
                "stack": 150,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "stack": 0,
                "bet": 0,
                "hole_cards": [
                    null,
                    null
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 2: Bet 41",
            "Player 0: Call 41"
        ],
        "terminal": false,
        "player": "Nature"
    }
    0: Showdown
    {
        "environment": {
            "min_delta": null,
            "pot": 0,
            "board": [
                "3d",
                "9h",
                "5h",
                "Kh",
                "8d"
            ],
            "aggressor": "Player 2"
        },
        "nature": {
            "nature": true,
            "index": null,
            "payoff": 0,
            "actions": []
        },
        "players": [
            {
                "nature": false,
                "index": 0,
                "payoff": 57,
                "actions": [],
                "stack": 257,
                "bet": 0,
                "hole_cards": [
                    "4s",
                    "8h"
                ]
            },
            {
                "nature": false,
                "index": 1,
                "payoff": -7,
                "actions": [],
                "stack": 93,
                "bet": 0,
                "hole_cards": null
            },
            {
                "nature": false,
                "index": 2,
                "payoff": -50,
                "actions": [],
                "stack": 0,
                "bet": 0,
                "hole_cards": [
                    "7s",
                    "3c"
                ]
            }
        ],
        "logs": [
            "Nature: Deal 2 hole cards and 0 board cards",
            "Player 2: Raise 4",
            "Player 0: Call 3",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 3 board cards",
            "Player 0: Check",
            "Player 1: Check",
            "Player 2: Bet 2",
            "Player 0: Call 2",
            "Player 1: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Bet 2",
            "Player 1: Fold",
            "Player 2: Call 2",
            "Nature: Deal 0 hole cards and 1 board cards",
            "Player 0: Check",
            "Player 2: Bet 41",
            "Player 0: Call 41",
            "Nature: Showdown"
        ],
        "terminal": true,
        "player": null
    }
