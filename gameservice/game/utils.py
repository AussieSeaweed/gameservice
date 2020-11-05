class Log:
    def __init__(self, action):
        self.__action_str = str(action)
        self.__player_str = str(action.player)

    def __str__(self):
        return f"{self.__player_str}: {self.__action_str}"


def nested_str(o, lim=None, level=0):
    if isinstance(o, list):
        o = dict(enumerate(o))

    if isinstance(o, dict) and lim != level:
        result = ""

        for key, value in o.items():
            result += "\t" * level + str(key) + "\n" + nested_str(value, lim, level + 1) + "\n"

        return result.rstrip()
    else:
        return "\t" * level + str(o)
