class Log:
    def __init__(self, action):
        self.__action_str = str(action)
        self.__player_str = str(action.player)

    def __str__(self):
        return f'{self.__player_str}: {self.__action_str}'
