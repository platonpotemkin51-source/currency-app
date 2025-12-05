import unittest
import sys
import os
from unittest.mock import Mock, patch
from io import BytesIO

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import SimpleHTTPRequestHandler
from models import User, Currency, UserCurrency, Author, App


class TestHTTPHandler(unittest.TestCase):
    """Тестирование HTTP-обработчика запросов"""

    def setUp(self):
        """Очистка хранилищ перед каждым тестом"""
        User._User__users = {}
        User._User__next_id = 0
        Currency._Currency__currencies = {}
        Currency._Currency__next_id = 0
        UserCurrency._UserCurrency__subscriptions = {}
        UserCurrency._UserCurrency__history = []

        # Создаем тестовые данные
        self.user1 = User.create("Иван Иванов", "ivan@test.com")
        self.user2 = User.create("Петр Петров", "petr@test.com")
        self.currency1 = Currency.create("840", "USD", "Доллар США", 75.50, 1)
        self.currency2 = Currency.create("978", "EUR", "Евро", 85.20, 1)
        
        # Подписываем пользователей на валюты
        UserCurrency.subscribe(self.user1.id, self.currency1.id)
        UserCurrency.subscribe(self.user1.id, self.currency2.id)

    def create_mock_handler(self, path):
        """Создает mock-объект для HTTP-обработчика"""
        handler = SimpleHTTPRequestHandler.__new__(SimpleHTTPRequestHandler)
        handler.path = path
        handler.wfile = BytesIO()
        handler.headers = {}
        handler.send_response = Mock()
        handler.send_header = Mock()
        handler.end_headers = Mock()
        return handler

    def test_do_get_home_page(self):
        """Проверка обработки GET-запроса к главной странице"""
        handler = self.create_mock_handler('/')
        
        # Вызываем метод обработки GET-запроса
        with patch('main.env') as mock_env:
            template_mock = Mock()
            template_mock.render.return_value = '<html>Test Home Page</html>'
            mock_env.get_template.return_value = template_mock
            
            handler.do_GET()
            
            # Проверяем, что шаблон был получен
            mock_env.get_template.assert_called_once_with("index.html")
            
            # Проверяем, что render был вызван с правильными параметрами
            template_mock.render.assert_called_once()
            call_args = template_mock.render.call_args[1]
            self.assertIn('flag', call_args)
            self.assertTrue(call_args['flag'])  # На главной странице flag должен быть True
            self.assertIn('currencies_count', call_args)
            self.assertIn('users_count', call_args)
            self.assertIsInstance(call_args['app'], App)

    def test_do_get_author_page(self):
        """Проверка обработки GET-запроса к странице автора"""
        handler = self.create_mock_handler('/author')
        
        with patch('main.env') as mock_env:
            template_mock = Mock()
            template_mock.render.return_value = '<html>Test Author Page</html>'
            mock_env.get_template.return_value = template_mock
            
            handler.do_GET()
            
            # Проверяем, что шаблон был получен
            mock_env.get_template.assert_called_once_with("index.html")
            
            # Проверяем, что render был вызван с правильными параметрами
            template_mock.render.assert_called_once()
            call_args = template_mock.render.call_args[1]
            self.assertNotIn('flag', call_args)  # На странице автора flag не передается
            self.assertIn('currencies_count', call_args)
            self.assertIn('users_count', call_args)
            self.assertIsInstance(call_args['app'], App)

    def test_do_get_currencies_page(self):
        """Проверка обработки GET-запроса к странице валют"""
        handler = self.create_mock_handler('/currencies')
        
        with patch('main.env') as mock_env:
            template_mock = Mock()
            template_mock.render.return_value = '<html>Test Currencies Page</html>'
            mock_env.get_template.return_value = template_mock
            
            handler.do_GET()
            
            # Проверяем, что шаблон был получен
            mock_env.get_template.assert_called_once_with("currencies.html")
            
            # Проверяем, что render был вызван с правильными параметрами
            template_mock.render.assert_called_once()
            call_args = template_mock.render.call_args[1]
            self.assertIn('currencies', call_args)
            self.assertIn('currencies_count', call_args)
            self.assertEqual(call_args['currencies_count'], 2)

    def test_do_get_users_page(self):
        """Проверка обработки GET-запроса к странице пользователей"""
        handler = self.create_mock_handler('/users')
        
        with patch('main.env') as mock_env:
            template_mock = Mock()
            template_mock.render.return_value = '<html>Test Users Page</html>'
            mock_env.get_template.return_value = template_mock
            
            handler.do_GET()
            
            # Проверяем, что шаблон был получен
            mock_env.get_template.assert_called_once_with("users.html")
            
            # Проверяем, что render был вызван с правильными параметрами
            template_mock.render.assert_called_once()
            call_args = template_mock.render.call_args[1]
            self.assertIn('users', call_args)
            self.assertIn('users_count', call_args)
            self.assertEqual(call_args['users_count'], 2)

    def test_do_get_user_page(self):
        """Проверка обработки GET-запроса к странице пользователя"""
        # Формируем путь с ID пользователя
        user_path = f'/user?id={self.user1.id}'
        handler = self.create_mock_handler(user_path)
        
        with patch('main.env') as mock_env:
            template_mock = Mock()
            template_mock.render.return_value = '<html>Test User Page</html>'
            mock_env.get_template.return_value = template_mock
            
            handler.do_GET()
            
            # Проверяем, что шаблон был получен
            mock_env.get_template.assert_called_once_with("user.html")
            
            # Проверяем, что render был вызван с правильными параметрами
            template_mock.render.assert_called_once()
            call_args = template_mock.render.call_args[1]
            self.assertIn('user', call_args)
            self.assertIn('currencies', call_args)
            self.assertIn('sub', call_args)
            self.assertEqual(call_args['user'].id, self.user1.id)
            self.assertEqual(call_args['user'].name, "Иван Иванов")

    def test_do_get_unknown_path(self):
        """Проверка обработки GET-запроса к неизвестному пути"""
        handler = self.create_mock_handler('/unknown')
        
        # Даже при неизвестном пути, обработчик должен выполниться без ошибок
        with patch('main.env') as mock_env:
            template_mock = Mock()
            template_mock.render.return_value = '<html>Test Page</html>'
            mock_env.get_template.return_value = template_mock
            
            # Проверяем, что при неизвестном пути не возникает ошибки
            handler.do_GET()
            
            # При неизвестном пути в текущей реализации код не найдет совпадений и 
            # не вызовет template.render, но ошибки не будет


class TestHTTPHandlerWithNoData(unittest.TestCase):
    """Тестирование HTTP-обработчика при отсутствии данных"""

    def setUp(self):
        """Очистка хранилищ перед каждым тестом"""
        User._User__users = {}
        User._User__next_id = 0
        Currency._Currency__currencies = {}
        Currency._Currency__next_id = 0
        UserCurrency._UserCurrency__subscriptions = {}
        UserCurrency._UserCurrency__history = []

    def create_mock_handler(self, path):
        """Создает mock-объект для HTTP-обработчика"""
        handler = SimpleHTTPRequestHandler.__new__(SimpleHTTPRequestHandler)
        handler.path = path
        handler.wfile = BytesIO()
        handler.headers = {}
        handler.send_response = Mock()
        handler.send_header = Mock()
        handler.end_headers = Mock()
        return handler

    def test_do_get_pages_with_no_data(self):
        """Проверка обработки страниц при отсутствии данных"""
        pages_to_test = ['/', '/author', '/currencies', '/users']
        
        for page_path in pages_to_test:
            with self.subTest(path=page_path):
                handler = self.create_mock_handler(page_path)
                
                with patch('main.env') as mock_env:
                    template_mock = Mock()
                    template_mock.render.return_value = '<html>Test Page</html>'
                    mock_env.get_template.return_value = template_mock
                    
                    # Должно выполниться без ошибок даже при отсутствии данных
                    handler.do_GET()
                    
                    # Проверяем, что методы ответа были вызваны
                    handler.send_response.assert_called()
                    handler.send_header.assert_called()
                    handler.end_headers.assert_called()


if __name__ == '__main__':
    unittest.main()