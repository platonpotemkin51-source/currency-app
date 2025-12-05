class User:
    __users = {}  # {id: User_object}
    __next_id = 0

    def __init__(self, user_id: int, name: str, email: str):
        self.__id = user_id
        self.__name = name
        self.__email = email

    # === СВОЙСТВА ДЛЯ ДОСТУПА К ДАННЫМ ===
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str) or len(name.strip()) < 2:
            raise ValueError("Имя должно быть строкой не менее 2 символов")
        self.__name = name.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise ValueError("Email должен быть корректной электронной почтой")
        self.__email = value

    # === СТАТИЧЕСКИЕ МЕТОДЫ ДЛЯ РАБОТЫ С ХРАНИЛИЩЕМ ===
    @classmethod
    def create(cls, name: str, email: str):
        """Создает и сохраняет нового пользователя"""
        if not cls.__users:
            cls.__users = {}

            # Проверка уникальности email
        for user in cls.__users.values():
            if user.email == email:
                raise ValueError("Пользователь с таким email уже существует")

        user_id = cls.__next_id
        cls.__next_id += 1
        user = cls(user_id, name, email)
        cls.__users[user_id] = user

        return user

    @classmethod
    def find_by_id(cls, user_id: int):
        """Находит пользователя по ID"""
        return cls.__users.get(user_id)

    @classmethod
    def find_by_email(cls, email: str):
        """Находит пользователя по email"""
        for user in cls.__users.values():
            if user.email == email:
                return user
        return None

    @classmethod
    def get_all(cls):
        """Возвращает всех пользователей"""
        return list(cls.__users.values())

    @classmethod
    def delete(cls, user_id: int):
        """Удаляет пользователя"""
        if user_id in cls.__users:
            del cls.__users[user_id]
            return True
        return False

test_users = [
    {"name":"Старожилов Аркадий", "email":"star_ar@mail.com"},
    {"name":"Лукьянов Александр", "email":"lukaki@mail.com"},
    {"name":"Аветисян Владислав", "email":"avet@mail.com"},
    {"name":"Пузиков Ярослав", "email":"yarei@mail.com"},
    {"name":"Потёмкин Платон", "email":"spbsvu3skype2@mail.com"}
]
for test_user in test_users:
    User.create(test_user["name"], test_user["email"])
# for user in User.get_all():
#     print(user.name)