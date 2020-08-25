class Actions:
    def __init__(self, actions):
        self.__actions = actions

    def __len__(self):
        return len(self.__actions)

    def __getitem__(self, item):
        return self.__actions[item]

    def __iter__(self):
        return iter(self.__actions)
