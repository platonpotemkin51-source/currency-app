import unittest
import sys
import os
from unittest.mock import patch, Mock

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.currencies_api import get_all_currencies_data, update_all_currencies
from models import User, UserCurrency, Currency


class TestCurrenciesUtils(unittest.TestCase):
    """Тестирование вспомогательных функций для работы с валютами"""

    def setUp(self):
        """Очистка хранилища перед каждым тестом"""
        from models import Currency
        Currency._Currency__currencies = {}
        Currency._Currency__next_id = 0

    @patch('utils.currencies_api.get_currencies')
    def test_get_all_currencies_data_success(self, mock_get_currencies):
        """Проверка получения всех данных о валютах"""
        mock_get_currencies.return_value = {
            'USD': {
                'ID': 'R01235',
                'NumCode': '840',
                'CharCode': 'USD',
                'Nominal': 1,
                'Name': 'Доллар США',
                'Value': 75.50,
                'Previous': 75.25
            },
            'EUR': {
                'ID': 'R01239',
                'NumCode': '978',
                'CharCode': 'EUR',
                'Nominal': 1,
                'Name': 'Евро',
                'Value': 85.20,
                'Previous': 85.00
            }
        }

        result = get_all_currencies_data()

        self.assertEqual(len(result), 2)
        usd_data = next(item for item in result if item['char_code'] == 'USD')
        self.assertEqual(usd_data['num_code'], '840')
        self.assertEqual(usd_data['name'], 'Доллар США')
        self.assertEqual(usd_data['value'], 75.50)
        self.assertEqual(usd_data['nominal'], 1)

        eur_data = next(item for item in result if item['char_code'] == 'EUR')
        self.assertEqual(eur_data['num_code'], '978')
        self.assertEqual(eur_data['name'], 'Евро')
        self.assertEqual(eur_data['value'], 85.20)
        self.assertEqual(eur_data['nominal'], 1)

    @patch('utils.currencies_api.get_currencies')
    def test_get_all_currencies_data_exception(self, mock_get_currencies):
        """Проверка обработки исключения при получении данных о валютах"""
        mock_get_currencies.side_effect = Exception("Test error")

        with self.assertRaises(ValueError) as context:
            get_all_currencies_data()

        self.assertIn("Ошибка при получении данных о валютах", str(context.exception))

    @patch('utils.currencies_api.get_all_currencies_data')
    @patch('models.currency.Currency.find_by_char_code')
    @patch('models.currency.Currency.create')
    def test_update_all_currencies_new_currency(self, mock_create, mock_find_by_char_code, mock_get_all_currencies_data):
        """Проверка обновления валют, когда валюта не найдена (создание новой)"""
        mock_get_all_currencies_data.return_value = [
            {
                'num_code': '840',
                'char_code': 'USD',
                'name': 'Доллар США',
                'value': 75.50,
                'nominal': 1
            }
        ]
        mock_find_by_char_code.return_value = None  # Валюта не найдена

        result = update_all_currencies()

        self.assertTrue(result)
        mock_create.assert_called_once_with(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=75.50,
            nominal=1
        )

    @patch('utils.currencies_api.get_all_currencies_data')
    @patch('models.currency.Currency.find_by_char_code')
    def test_update_all_currencies_existing_currency(self, mock_find_by_char_code, mock_get_all_currencies_data):
        """Проверка обновления валют, когда валюта найдена (обновление существующей)"""
        from models import Currency
        
        # Создаем тестовую валюту
        currency = Currency.create("840", "USD", "Доллар США", 70.0, 1)
        
        mock_get_all_currencies_data.return_value = [
            {
                'num_code': '840',
                'char_code': 'USD',
                'name': 'Доллар США',
                'value': 75.50,
                'nominal': 1
            }
        ]
        mock_find_by_char_code.return_value = currency

        result = update_all_currencies()

        self.assertTrue(result)
        self.assertEqual(currency.value, 75.50)  # Проверяем, что значение обновилось


class TestUserCurrencyExtended(unittest.TestCase):
    """Дополнительное тестирование класса UserCurrency"""

    def setUp(self):
        """Очистка хранилища перед каждым тестом"""
        from models import UserCurrency, User, Currency
        UserCurrency._UserCurrency__subscriptions = {}
        UserCurrency._UserCurrency__history = []

        # Сбросить хранилища других классов
        User._User__users = {}
        User._User__next_id = 0
        Currency._Currency__currencies = {}
        Currency._Currency__next_id = 0

        # Создать тестовые данные
        self.user = User.create("Иван Иванов", "ivan@test.com")
        self.currency = Currency.create("840", "USD", "Доллар США", 75.50, 1)

    def test_get_subscription_history_for_user(self):
        """Проверка получения истории подписок для конкретного пользователя"""
        # Подписываем пользователя на валюту
        UserCurrency.subscribe(self.user.id, self.currency.id)
        
        # Получаем общую историю
        all_history = UserCurrency.get_subscription_history()
        # Получаем историю для конкретного пользователя
        user_history = UserCurrency.get_subscription_history(self.user.id)
        # Получаем историю для несуществующего пользователя
        empty_history = UserCurrency.get_subscription_history(999)
        
        self.assertEqual(len(all_history), 1)
        self.assertEqual(len(user_history), 1)
        self.assertEqual(len(empty_history), 0)
        self.assertEqual(all_history[0], user_history[0])

    def test_get_subscription_history_all_users(self):
        """Проверка получения всей истории подписок"""
        user2 = User.create("Петр Петров", "petr@test.com")
        currency2 = Currency.create("978", "EUR", "Евро", 85.20, 1)
        
        UserCurrency.subscribe(self.user.id, self.currency.id)
        UserCurrency.subscribe(user2.id, currency2.id)
        UserCurrency.unsubscribe(self.user.id, self.currency.id)
        
        all_history = UserCurrency.get_subscription_history()
        
        self.assertEqual(len(all_history), 3)  # 2 подписки + 1 отписка
        self.assertEqual(all_history[0]['user_id'], self.user.id)
        self.assertEqual(all_history[1]['user_id'], user2.id)
        self.assertEqual(all_history[2]['user_id'], self.user.id)
        self.assertEqual(all_history[2]['action'], 'unsubscribe')


if __name__ == '__main__':
    unittest.main()