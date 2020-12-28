from json import dumps
from typing import Any, Dict


def print_information_set(information_set: Dict[str, Any], indent=4):
    print(dumps(information_set, indent=indent))
