from models import User
from models import Currency


class UserCurrency:
    __subscriptions = {}  # {user_id: [currency_id, ...]}
    __history = []  # История изменений подписок

    def __init__(self, user_id: int, currency_id: int):
        self.__user_id = user_id
        self.__currency_id = currency_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def currency_id(self):
        return self.__currency_id

    @classmethod
    def subscribe(cls, user_id: int, currency_id: int):
        """Добавляет подписку пользователя на валюту"""
        user = User.find_by_id(user_id)
        currency = Currency.find_by_id(currency_id)

        if not user or not currency:
            return False

        if user_id not in cls.__subscriptions:
            cls.__subscriptions[user_id] = []

        if currency_id not in cls.__subscriptions[user_id]:
            cls.__subscriptions[user_id].append(currency_id)
            # Сохраняем в историю
            cls.__history.append({
                'user_id': user_id,
                'currency_id': currency_id,
                'action': 'subscribe',
                'timestamp': cls._get_timestamp()
            })
            return True
        return False

    @classmethod
    def unsubscribe(cls, user_id: int, currency_id: int):
        """Удаляет подписку пользователя на валюту"""
        if user_id in cls.__subscriptions and currency_id in cls.__subscriptions[user_id]:
            cls.__subscriptions[user_id].remove(currency_id)
            # Сохраняем в историю
            cls.__history.append({
                'user_id': user_id,
                'currency_id': currency_id,
                'action': 'unsubscribe',
                'timestamp': cls._get_timestamp()
            })
            return True
        return False

    @classmethod
    def get_user_subscriptions(cls, user_id: int):
        """Возвращает список подписок пользователя"""
        currency_ids = cls.__subscriptions.get(user_id, [])
        subscriptions = []

        for currency_id in currency_ids:
            currency = Currency.find_by_id(currency_id)
            if currency:
                subscriptions.append(currency.to_dict())

        return subscriptions

    @classmethod
    def get_subscription_history(cls, user_id: int = None):
        """Возвращает историю подписок"""
        if user_id is None:
            return cls.__history
        return [item for item in cls.__history if item['user_id'] == user_id]

    @classmethod
    def is_subscribed(cls, user_id: int, currency_id: int):
        """Проверяет, подписан ли пользователь на валюту"""
        if user_id in cls.__subscriptions:
            return currency_id in cls.__subscriptions[user_id]
        return False

    @classmethod
    def _get_timestamp(cls):
        """Возвращает текущее время в формате строки"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_currency_trend(cls, currency_id: int, days: int = 7):
        """Возвращает динамику изменения валюты за указанный период"""
        # В реальном приложении здесь был бы запрос к БД
        # Для примезаем статические данные
        import random
        trend = []
        base_value = 70.0

        for i in range(days):
            trend.append({
                'date': f"Day {i + 1}",
                'value': base_value + random.uniform(-5, 5)
            })

        return trend

test_user_subscriptions = [
    {
        'user_id': 0,
        'currency_id': [0, 1, 2, 3, 4]
    },
    {
        'user_id': 1,
        'currency_id': [1, 3]
    },
    {
        'user_id': 2,
        'currency_id': [19, 3, 25, 44, 53]
    },
    {
        'user_id': 3,
        'currency_id': [34, 28]
    },
    {
        'user_id': 4,
        'currency_id': [0, 32, 15, 50]
    }
]
for test in test_user_subscriptions:
    for i in test['currency_id']:
        UserCurrency.subscribe(test['user_id'], i)

k = []

id = 0



for i in UserCurrency.get_user_subscriptions(0):
    k.append(i['char_code'])

# print(', '.join(k))
# print (len(UserCurrency.get_user_subscriptions(0)))
# print('qwqweqwe')