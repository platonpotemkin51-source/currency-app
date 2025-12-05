# utils/currencies_api.py
import requests
import json
import sys
from typing import List, Dict


def get_currencies(currency_codes: list = None,
                   url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
                   handle=sys.stdout,
                   test_response: dict = None) -> dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
                              Если None, возвращает все валюты.
        url (str): URL API
        handle: Поток для вывода (по умолчанию sys.stdout)
        test_response (dict): Тестовые данные для отладки

    Returns:
        dict: Словарь с данными о валютах.
              Возвращает None в случае ошибки запроса.
    """
    # Если переданы тестовые данные, используем их
    if test_response is not None:
        data = test_response
    else:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Выбрасывает HTTPError при статусе != 200
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            raise ConnectionError(f"API недоступно: {str(e)}")

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON в ответе: {str(e)}")

    if "Valute" not in data:
        raise KeyError("Ключ 'Valute' отсутствует в ответе API")

    # Если currency_codes не указан, возвращаем все валюты
    if currency_codes is None:
        currencies = {}
        for code, valute_data in data["Valute"].items():
            currencies[code] = {
                'ID': valute_data.get('ID', ''),
                'NumCode': valute_data.get('NumCode', ''),
                'CharCode': valute_data.get('CharCode', ''),
                'Nominal': valute_data.get('Nominal', 1),
                'Name': valute_data.get('Name', ''),
                'Value': valute_data.get('Value', 0.0),
                'Previous': valute_data.get('Previous', 0.0)
            }
        return currencies

    # Если указаны конкретные коды
    currencies = {}

    for code in currency_codes:
        code = code.upper()
        if code in data["Valute"]:
            currencies[code] = data["Valute"][code]["Value"]
        else:
            raise KeyError(f"Валюта '{code}' отсутствует в данных ЦБ")

        try:
            nomb = float(currencies[code])
        except:
            raise TypeError(
                f"Курс валюты '{code}' имеет неверный тип: {type(currencies[code])}"
            )

    return currencies


# Вспомогательные функции для работы с get_currencies
def get_all_currencies_data() -> List[Dict]:
    """Получает полные данные по всем валютам используя get_currencies"""
    try:
        currencies_dict = get_currencies(currency_codes=None)
        currencies_list = []

        for code, data in currencies_dict.items():
            currencies_list.append({
                'num_code': data.get('NumCode', ''),
                'char_code': data.get('CharCode', ''),
                'name': data.get('Name', ''),
                'value': data.get('Value', 0.0),
                'nominal': data.get('Nominal', 1),
            })

        return currencies_list

    except Exception as e:
        raise ValueError(f"Ошибка при получении данных о валютах: {e}")



def update_all_currencies() -> bool:
    """
    Обновляет курсы всех валют в базе данных используя get_currencies
    """
    try:
        from models import Currency

        currencies_data = get_all_currencies_data()

        for currency_data in currencies_data:
            # Ищем валюту по символьному коду
            currency = Currency.find_by_char_code(currency_data['char_code'])

            if currency:
                # Обновляем курс
                currency.value = currency_data['value']
            else:
                # Создаем новую валюту
                Currency.create(
                    num_code=currency_data['num_code'],
                    char_code=currency_data['char_code'],
                    name=currency_data['name'],
                    value=currency_data['value'],
                    nominal=currency_data['nominal']
                )

        return True

    except Exception as e:
        print(f"Ошибка при обновлении валют: {e}")
        return False