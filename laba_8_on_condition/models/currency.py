from utils.currencies_api import *

class Currency:
    __currencies = {}  # Хранилище валют {id: currency_object}
    __next_id = 0


    def __init__(self, id: int, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__id = id
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def id(self):
        return self.__id

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, value):
        if not isinstance(value, str) or len(value) != 3 or not value.isdigit():
            raise ValueError("Цифровой код должен быть строкой из 3 цифр")
        self.__num_code = value

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, value):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError("Символьный код должен быть строкой из 3 символов")
        self.__char_code = value.upper()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Название валюты не может быть пустым")
        self.__name = value.strip()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Курс должен быть положительным числом")
        self.__value = float(value)

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номинал должен быть положительным целым числом")
        self.__nominal = value

    @classmethod
    def create(cls, num_code: str, char_code: str, name: str, value: float, nominal: int = 1):
        """Создает новую валюту"""
        if not cls.__currencies:
            cls.__currencies = {}

        currency_id = cls.__next_id
        cls.__next_id += 1
        currency = cls(currency_id, num_code, char_code, name, value, nominal)
        cls.__currencies[currency_id] = currency
        return currency

    @classmethod
    def find_by_id(cls, currency_id: int):
        """Находит валюту по ID"""
        return cls.__currencies.get(currency_id)

    @classmethod
    def find_by_char_code(cls, char_code: str):
        """Находит валюту по символьному коду"""
        for currency in cls.__currencies.values():
            if currency.char_code == char_code.upper():
                return currency
        return None

    @classmethod
    def get_all(cls):
        """Возвращает все валюты"""
        return list(cls.__currencies.values())

    @classmethod
    def update_rate(cls, currency_id: int, new_value: float):
        """Обновляет курс валюты"""
        currency = cls.find_by_id(currency_id)
        if currency:
            currency.value = new_value
            return True
        return False

    def to_dict(self):
        """Преобразует объект в словарь"""
        return {
            'id': self.id,
            'num_code': self.num_code,
            'char_code': self.char_code,
            'name': self.name,
            'value': self.value,
            'nominal': self.nominal,
            'rate_per_unit': self.value / self.nominal
        }

for currency in get_all_currencies_data():
    Currency.create(**currency)
# for currency in Currency.get_all():
#     print(currency.to_dict())