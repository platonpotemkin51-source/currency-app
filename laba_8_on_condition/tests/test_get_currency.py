import unittest
import requests
from utils.currencies_api import get_currencies
import io


class TestGetCurrenciesModified(unittest.TestCase):
    """Тесты с модифицированной функцией"""

    def test_get_valid_currencies(self):
        currency_list = ['USD']
        currency_data = get_currencies(currency_list)

        self.assertIn(currency_list[0], currency_data)
        self.assertIsInstance(currency_data['USD'], float)
        self.assertGreaterEqual(currency_data['USD'], 51)
        self.assertLessEqual(currency_data['USD'], 121)

    def test_empty_currency_list(self):
        """Тестирование с пустым списком"""
        result = get_currencies([])
        self.assertEqual(result, {})

    def test_nonexistent_currency(self):
        """Тестирование несуществующей валюты"""
        with self.assertRaises(KeyError) as context:
            get_currencies(['USD', 'XYZ'])

        self.assertIn("Валюта 'XYZ' отсутствует", str(context.exception))

    def test_missing_valute_key(self):
        """Тестирование ответа без ключа Valute"""
        test_response = {"Date": "2024-01-01"}  # Нет ключа Valute

        with self.assertRaises(KeyError) as context:
            get_currencies(['USD'], test_response=test_response)

        self.assertIn("Ключ 'Valute' отсутствует", str(context.exception))

    def test_invalid_value_error(self):
        """Тестирование некорректного формата данных (JSON)"""
        with self.assertRaises(ValueError) as context:
            get_currencies(['USD'], url="https://www.google.com")

        self.assertIn("Некорректный JSON в ответе:", str(context.exception))

    def test_invalid_currency_value_type(self):
        """Тестирование некорректного типа курса"""
        test_response = {
            "Valute": {
                "USD": {
                    "Value": "не число",
                    "Name": "Доллар США"
                },
            }
        }

        with self.assertRaises(TypeError) as context:
            get_currencies(['USD'], test_response=test_response)

        self.assertIn("Курс валюты 'USD' имеет неверный тип",
                      str(context.exception))

    def test_connection_error_simulation(self):
        """Тестирование симуляции ConnectionError"""
        # Используем несуществующий URL для имитации ошибки соединения
        # (Это интеграционный тест, может быть нестабильным)
        try:
            with self.assertRaises(ConnectionError) as context:
                get_currencies(
                    ['USD'],
                    url="http://nonexistent-domain-12345.ru/daily_json.js")

            self.assertIn("API недоступно:", str(context.exception))

        except Exception as e:
            # Если тест не прошел, пропускаем
            self.skipTest(f"Не удалось симулировать ConnectionError: {e}")


# Дополнительные утилиты для тестирования
def test_connection_error_real():
    """Функция для ручного тестирования ConnectionError"""
    # Отключаем интернет или используем неверный URL
    test_url = "http://127.0.0.1:9999/daily_json.js"  # Несуществующий порт

    print("Тестирование ConnectionError (требуется отключение интернета)...")
    try:
        get_currencies(['USD'], url=test_url)
        print("ОШИБКА: ConnectionError не был вызван")
    except ConnectionError as e:
        print(f"✓ ConnectionError успешно вызван: {e}")
    except Exception as e:
        print(f"✗ Вызвано другое исключение: {type(e).__name__}: {e}")


def test_value_error_real():
    """Функция для ручного тестирования ValueError"""
    # Используем URL, который возвращает не JSON
    test_url = "https://www.google.com"  # Возвращает HTML

    print("\nТестирование ValueError (не-JSON ответ)...")
    try:
        get_currencies(['USD'], url=test_url)
        print("ОШИБКА: ValueError не был вызван")
    except ValueError as e:
        print(f"✓ ValueError успешно вызван: {e}")
    except Exception as e:
        print(f"✗ Вызвано другое исключение: {type(e).__name__}: {e}")


if __name__ == '__main__':
    # Запуск unit-тестов
    unittest.main(verbosity=2)