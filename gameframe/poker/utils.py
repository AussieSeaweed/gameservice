import re
from collections.abc import Iterable

from pokertools import parse_cards

from gameframe.poker.bases import Poker, PokerPlayer


def parse_poker(game: Poker, tokens: Iterable[str]) -> Poker:
    """Parses the tokens as actions and applies them the supplied poker game.

    :param game: The poker game to be applied on.
    :param tokens: The tokens to parse as actions.
    :return: None.
    """
    for token in tokens:
        if isinstance(game._actor, PokerPlayer):
            if match := re.fullmatch(r'br( (?P<amount>\d+))?', token):
                game._actor.bet_raise(None if (amount := match.group('amount')) is None else int(amount))
            elif token == 'cc':
                game._actor.check_call()
            elif token == 'f':
                game._actor.fold()
            elif match := re.fullmatch(r'd( (?P<froms>\w*))?( (?P<tos>\w*))?', token):
                game._actor.draw(
                    () if (cards := match.group('froms')) is None else parse_cards(cards),
                    None if (cards := match.group('tos')) is None else parse_cards(cards),
                )
            elif match := re.fullmatch(r's( (?P<force>[0|1]))?', token):
                game._actor.showdown(False if (force := match.group('force')) is None else bool(force))
            else:
                raise ValueError('Invalid command')
        else:
            if match := re.fullmatch(r'dh (?P<index>\d+)( (?P<cards>\w+))?', token):
                game.nature.deal_hole(
                    game.players[int(match.group('index'))],
                    None if (cards := match.group('cards')) is None else parse_cards(cards),
                )
            elif match := re.fullmatch(r'db( (?P<cards>\w+))?', token):
                game.nature.deal_board(None if (cards := match.group('cards')) is None else parse_cards(cards))
            else:
                raise ValueError('Invalid command')

    return game
