from typing import TypeVar
import re

from pokertools import parse_card

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
            if match := re.match(r'br (?P<amount>\d+)', token):
                game.actor.bet_raise(int(match.group('amount')))
            elif token == 'cc':
                game.actor.check_call()
            elif token == 'f':
                game.actor.fold()
            elif match := re.match(r's( (?P<force>[0|1]))?', token):
                game.actor.showdown(False if match.group('force') is None else bool(match.group('force')))
            else:
                raise ValueError('Invalid command')
        else:
            if match := re.match(r'dp (?P<index>\d+) (?P<cards_raw>\w+)', token):
                cards_raw = match.group('cards_raw')
                cards = []

                for i in range(0, len(cards_raw), 2):
                    cards.append(parse_card(cards_raw[i:i + 2]))

                game.nature.deal_player(game.players[int(match.group('index'))], *cards)
            elif match := re.match(r'db (?P<cards_raw>\w+)', token):
                cards_raw = match.group('cards_raw')
                cards = []

                for i in range(0, len(cards_raw), 2):
                    cards.append(parse_card(cards_raw[i:i + 2]))

                game.nature.deal_board(*cards)
            else:
                raise ValueError('Invalid command')
