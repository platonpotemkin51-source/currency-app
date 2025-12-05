class App:
    def __init__(self, name: str, version: str, author):
        self.__name = name
        self.__version = version
        self.__author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Название приложения должно быть строкой не менее 1 символа")
        self.__name = value.strip()

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        if not isinstance(value, str):
            raise ValueError("Версия должна быть строкой")
        # Проверка формата версии (например, "1.0.0")
        parts = value.split('.')
        if not all(part.isdigit() for part in parts):
            raise ValueError("Версия должна быть в формате X.Y.Z")
        self.__version = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        from .author import Author
        if not isinstance(value, Author):
            raise ValueError("Автор должен быть объектом класса Author")
        self.__author = value