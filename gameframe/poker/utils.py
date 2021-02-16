import re
from typing import TypeVar

from pokertools import parse_cards

from gameframe.poker import PokerGame, PokerPlayer

PG = TypeVar('PG', bound=PokerGame)


def parse_poker_game(game: PG, *tokens: str) -> None:
    """Parses the tokens as actions and applies them the supplied game.

    :param game: the game to be applied on
    :param tokens: the tokens to parse as actions
    :return: None
    """
    for token in tokens:
        if isinstance(game.actor, PokerPlayer):
            if match := re.fullmatch(r'br (?P<amount>\d+)', token):
                game.actor.bet_raise(int(match.group('amount')))
            elif token == 'cc':
                game.actor.check_call()
            elif token == 'f':
                game.actor.fold()
            elif match := re.fullmatch(r's( (?P<force>[0|1]))?', token):
                game.actor.showdown(False if match.group('force') is None else bool(match.group('force')))
            else:
                raise ValueError('Invalid command')
        else:
            if match := re.fullmatch(r'dp (?P<index>\d+) (?P<cards>\w+)', token):
                game.nature.deal_player(game.players[int(match.group('index'))], *parse_cards(match.group('cards')))
            elif match := re.fullmatch(r'db (?P<cards>\w+)', token):
                game.nature.deal_board(*parse_cards(match.group('cards')))
            else:
                raise ValueError('Invalid command')
