import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import *
from datetime import datetime


class TestAuthor(unittest.TestCase):
    """Тестирование класса Author"""

    def test_author_creation(self):
        """Проверка создания объекта Author"""
        author = Author("Потёмкин Платон", "P3122")
        self.assertEqual(author.name, "Потёмкин Платон")
        self.assertEqual(author.group, "P3122")

    def test_author_name_setter_valid(self):
        """Проверка сеттера имени с корректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        author.name = "Петр Петров"
        self.assertEqual(author.name, "Петр Петров")

    def test_author_name_setter_invalid(self):
        """Проверка сеттера имени с некорректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.name = ""
        self.assertIn("Имя не может быть меньше одного символа", str(context.exception))

    def test_author_group_setter_valid(self):
        """Проверка сеттера группы с корректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        author.group = "P3123"
        self.assertEqual(author.group, "P3123")

    def test_author_group_setter_invalid(self):
        """Проверка сеттера группы с некорректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.group = "P31222"  # 6 символов
        self.assertIn("Группа должна быть строкой и менее 5 символов", str(context.exception))


class TestApp(unittest.TestCase):
    """Тестирование класса App"""

    def test_app_creation(self):
        """Проверка создания объекта App"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        self.assertEqual(app.name, "Test App")
        self.assertEqual(app.version, "1.0.0")
        self.assertEqual(app.author, author)

    def test_app_name_setter_valid(self):
        """Проверка сеттера названия приложения"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        app.name = "New App Name"
        self.assertEqual(app.name, "New App Name")

    def test_app_name_setter_invalid(self):
        """Проверка сеттера названия приложения с некорректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.name = ""
        self.assertIn("Название приложения должно быть строкой не менее 1 символа", str(context.exception))

    def test_app_version_setter_valid(self):
        """Проверка сеттера версии с корректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        app.version = "2.1.5"
        self.assertEqual(app.version, "2.1.5")

    def test_app_version_setter_invalid(self):
        """Проверка сеттера версии с некорректным значением"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        with self.assertRaises(ValueError) as context:
            app.version = 1.0
        self.assertIn("Версия должна быть строкой", str(context.exception))


class TestUser(unittest.TestCase):
    """Тестирование класса User"""

    def setUp(self):
        """Очистка хранилища перед каждым тестом"""
        User._User__users = {}
        User._User__next_id = 0

    def test_user_creation(self):
        """Проверка создания объекта User"""
        user = User.create("Иван Иванов", "ivan@test.com")
        self.assertEqual(user.name, "Иван Иванов")
        self.assertEqual(user.email, "ivan@test.com")
        self.assertEqual(user.id, 0)

    def test_user_name_setter_valid(self):
        """Проверка сеттера имени пользователя"""
        user = User.create("Иван Иванов", "ivan@test.com")
        user.name = "Петр Петров"
        self.assertEqual(user.name, "Петр Петров")

    def test_user_name_setter_invalid(self):
        """Проверка сеттера имени с некорректным значением"""
        user = User.create("Иван Иванов", "ivan@test.com")
        with self.assertRaises(ValueError) as context:
            user.name = "Я"  # 1 символ
        self.assertIn("Имя должно быть строкой не менее 2 символов", str(context.exception))

    def test_user_email_setter_valid(self):
        """Проверка сеттера email"""
        user = User.create("Иван Иванов", "ivan@test.com")
        user.email = "new@test.com"
        self.assertEqual(user.email, "new@test.com")

    def test_user_email_setter_invalid(self):
        """Проверка сеттера email с некорректным значением"""
        user = User.create("Иван Иванов", "ivan@test.com")
        with self.assertRaises(ValueError) as context:
            user.email = "not-an-email"
        self.assertIn("Email должен быть корректной электронной почтой", str(context.exception))

    def test_find_by_id(self):
        """Проверка поиска пользователя по ID"""
        user1 = User.create("Иван Иванов", "ivan@test.com")
        user2 = User.create("Петр Петров", "petr@test.com")

        found = User.find_by_id(0)
        self.assertEqual(found, user1)
        self.assertEqual(found.name, "Иван Иванов")

        found = User.find_by_id(1)
        self.assertEqual(found, user2)

        found = User.find_by_id(999)
        self.assertIsNone(found)

    def test_find_by_email(self):
        """Проверка поиска пользователя по email"""
        User.create("Иван Иванов", "ivan@test.com")
        User.create("Петр Петров", "petr@test.com")

        found = User.find_by_email("ivan@test.com")
        self.assertEqual(found.name, "Иван Иванов")

        found = User.find_by_email("nonexistent@test.com")
        self.assertIsNone(found)

    def test_email_uniqueness(self):
        """Проверка уникальности email"""
        User.create("Иван Иванов", "ivan@test.com")
        with self.assertRaises(ValueError) as context:
            User.create("Другой Иван", "ivan@test.com")
        self.assertIn("Пользователь с таким email уже существует", str(context.exception))

    def test_get_all_users(self):
        """Проверка получения всех пользователей"""
        self.assertEqual(len(User.get_all()), 0)

        user1 = User.create("Иван Иванов", "ivan@test.com")
        user2 = User.create("Петр Петров", "petr@test.com")

        users = User.get_all()
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)

    def test_delete_user(self):
        """Проверка удаления пользователя"""
        user1 = User.create("Иван Иванов", "ivan@test.com")
        user2 = User.create("Петр Петров", "petr@test.com")

        self.assertTrue(User.delete(0))
        self.assertEqual(len(User.get_all()), 1)
        self.assertIsNone(User.find_by_id(0))

        self.assertFalse(User.delete(999))


class TestCurrency(unittest.TestCase):
    """Тестирование класса Currency"""

    def setUp(self):
        """Очистка хранилища перед каждым тестом"""
        Currency._Currency__currencies = {}
        Currency._Currency__next_id = 0

    def test_currency_creation(self):
        """Проверка создания объекта Currency"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        self.assertEqual(currency.num_code, "840")
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "Доллар США")
        self.assertEqual(currency.value, 75.50)
        self.assertEqual(currency.nominal, 1)
        self.assertEqual(currency.id, 0)

    def test_num_code_setter_invalid(self):
        """Проверка сеттера цифрового кода с некорректным значением"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        with self.assertRaises(ValueError) as context:
            currency.num_code = "12"  # Меньше 3 символов
        self.assertIn("Цифровой код должен быть строкой из 3 цифр", str(context.exception))

    def test_char_code_setter_valid(self):
        """Проверка сеттера символьного кода"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        currency.char_code = "EUR"
        self.assertEqual(currency.char_code, "EUR")

        # Проверка автоматического приведения к верхнему регистру
        currency.char_code = "gbp"
        self.assertEqual(currency.char_code, "GBP")

    def test_char_code_setter_invalid(self):
        """Проверка сеттера символьного кода с некорректным значением"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        with self.assertRaises(ValueError) as context:
            currency.char_code = "US"  # 2 символа
        self.assertIn("Символьный код должен быть строкой из 3 символов", str(context.exception))

    def test_name_setter_invalid(self):
        """Проверка сеттера названия с некорректным значением"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        with self.assertRaises(ValueError) as context:
            currency.name = ""
        self.assertIn("Название валюты не может быть пустым", str(context.exception))

    def test_value_setter_invalid(self):
        """Проверка сеттера курса с некорректным значением"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        with self.assertRaises(ValueError) as context:
            currency.value = -10
        self.assertIn("Курс должен быть положительным числом", str(context.exception))

    def test_nominal_setter_invalid(self):
        """Проверка сеттера номинала с некорректным значением"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        with self.assertRaises(ValueError) as context:
            currency.nominal = -1
        self.assertIn("Номинал должен быть положительным целым числом", str(context.exception))

    def test_find_by_id(self):
        """Проверка поиска валюты по ID"""
        currency1 = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        currency2 = Currency.create("978", "EUR", "Евро", 85.20, 1)

        found = Currency.find_by_id(0)
        self.assertEqual(found, currency1)
        self.assertEqual(found.char_code, "USD")

        found = Currency.find_by_id(999)
        self.assertIsNone(found)

    def test_find_by_char_code(self):
        """Проверка поиска валюты по символьному коду"""
        Currency.create("840", "USD", "Доллар США", 75.50, 1)
        Currency.create("978", "EUR", "Евро", 85.20, 1)

        found = Currency.find_by_char_code("USD")
        self.assertEqual(found.name, "Доллар США")

        found = Currency.find_by_char_code("eur")  # Проверка case-insensitive
        self.assertEqual(found.char_code, "EUR")

    def test_get_all_currencies(self):
        """Проверка получения всех валют"""
        self.assertEqual(len(Currency.get_all()), 0)

        currency1 = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        currency2 = Currency.create("978", "EUR", "Евро", 85.20, 1)

        currencies = Currency.get_all()
        self.assertEqual(len(currencies), 2)
        self.assertIn(currency1, currencies)
        self.assertIn(currency2, currencies)

    def test_update_rate(self):
        """Проверка обновления курса валюты"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)

        self.assertTrue(Currency.update_rate(0, 80.25))
        self.assertEqual(currency.value, 80.25)

        self.assertFalse(Currency.update_rate(999, 80.25))

    def test_to_dict(self):
        """Проверка преобразования в словарь"""
        currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        result = currency.to_dict()

        expected = {
            'id': 0,
            'num_code': '840',
            'char_code': 'USD',
            'name': 'Доллар США',
            'value': 75.50,
            'nominal': 1,
            'rate_per_unit': 75.50
        }

        self.assertEqual(result, expected)


class TestUserCurrency(unittest.TestCase):
    """Тестирование класса UserCurrency"""

    def setUp(self):
        """Очистка хранилища перед каждым тестом"""
        UserCurrency._UserCurrency__subscriptions = {}
        UserCurrency._UserCurrency__history = []

        # Сбросить хранилища других классов
        User._User__users = {}
        User._User__next_id = 0
        Currency._Currency__currencies = {}
        Currency._Currency__next_id = 0

        # Создать тестовые данные
        self.user1 = User.create("Иван Иванов", "ivan@test.com")
        self.user2 = User.create("Петр Петров", "petr@test.com")
        self.currency1 = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        self.currency2 = Currency.create("978", "EUR", "Евро", 85.20, 1)

    def test_subscribe_success(self):
        """Проверка успешной подписки"""
        self.assertTrue(UserCurrency.subscribe(self.user1.id, self.currency1.id))
        self.assertTrue(UserCurrency.is_subscribed(self.user1.id, self.currency1.id))

        # Проверка, что подписка добавлена в историю
        history = UserCurrency.get_subscription_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['user_id'], self.user1.id)
        self.assertEqual(history[0]['action'], 'subscribe')

    def test_subscribe_duplicate(self):
        """Проверка дублирующей подписки"""
        UserCurrency.subscribe(self.user1.id, self.currency1.id)
        self.assertFalse(UserCurrency.subscribe(self.user1.id, self.currency1.id))
        self.assertEqual(len(UserCurrency.get_subscription_history()), 1)

    def test_subscribe_invalid_user(self):
        """Проверка подписки с несуществующим пользователем"""
        self.assertFalse(UserCurrency.subscribe(999, self.currency1.id))

    def test_subscribe_invalid_currency(self):
        """Проверка подписки с несуществующей валютой"""
        self.assertFalse(UserCurrency.subscribe(self.user1.id, 999))

    def test_unsubscribe_success(self):
        """Проверка успешной отписки"""
        UserCurrency.subscribe(self.user1.id, self.currency1.id)
        self.assertTrue(UserCurrency.unsubscribe(self.user1.id, self.currency1.id))
        self.assertFalse(UserCurrency.is_subscribed(self.user1.id, self.currency1.id))

    def test_get_user_subscriptions(self):
        """Проверка получения подписок пользователя"""
        UserCurrency.subscribe(self.user1.id, self.currency1.id)
        UserCurrency.subscribe(self.user1.id, self.currency2.id)

        subscriptions1 = UserCurrency.get_user_subscriptions(self.user1.id)
        self.assertEqual(len(subscriptions1), 2)
        char_codes = [s['char_code'] for s in subscriptions1]
        self.assertIn('USD', char_codes)
        self.assertIn('EUR', char_codes)

    def test_is_subscribed(self):
        """Проверка наличия подписки"""
        UserCurrency.subscribe(self.user1.id, self.currency1.id)

        self.assertTrue(UserCurrency.is_subscribed(self.user1.id, self.currency1.id))
        self.assertFalse(UserCurrency.is_subscribed(self.user1.id, self.currency2.id))

    def test_get_currency_trend(self):
        """Проверка получения тренда валюты"""
        trend = UserCurrency.get_currency_trend(self.currency1.id, days=5)

        self.assertEqual(len(trend), 5)
        for day_data in trend:
            self.assertIn('date', day_data)
            self.assertIn('value', day_data)


if __name__ == '__main__':
    unittest.main()