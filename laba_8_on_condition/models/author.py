class Author():
    def __init__(self, name: str, group: str = "P3122"):
        # конструктор
        self.__name = name
        self.__group = group


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) >= 1:
            self.__name = name
        else:
            raise ValueError("Имя не может быть меньше одного символа")


    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group):
        if isinstance(group, str) and len(group) == 5:
            self.__group = group
        else:
            raise ValueError("Группа должна быть строкой и менее 5 символов")