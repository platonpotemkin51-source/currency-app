import pytest
import threading
import time
from http.server import HTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError
import sys
import os

# Добавим путь к основному модулю, если нужно
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import SimpleHTTPRequestHandler  # Убедись, что имя совпадает!
from models import User, Currency, UserCurrency


class TestServer:
    port = 8081
    server = None
    thread = None

    @classmethod
    def start_server(cls):
        cls.server = HTTPServer(('localhost', cls.port), SimpleHTTPRequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.3)  # дать серверу запуститься

    @classmethod
    def stop_server(cls):
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()

    @classmethod
    def make_request(cls, path):
        url = f"http://localhost:{cls.port}{path}"
        with urlopen(url) as resp:
            assert resp.getcode() == 200
            return resp.read().decode('utf-8')


@pytest.fixture(scope="session", autouse=True)
def run_server():
    """Запускает сервер один раз на всю сессию тестов."""
    TestServer.start_server()
    yield
    TestServer.stop_server()


def test_home_page():
    html = TestServer.make_request('/')
    assert 'First' in html
    assert '1.0.0' in html
    assert 'Platon Potemkin' in html


def test_author_page():
    html = TestServer.make_request('/author')
    assert 'Platon Potemkin' in html
    # Если в шаблоне при flag=False что-то скрывается — добавь проверку


def test_currencies_page():
    html = TestServer.make_request('/currencies')

    # Обязательно: убедимся, что страница загружается
    assert '<html' in html.lower()

    # Проверим, что шаблон пытается отобразить данные
    currencies = Currency.get_all()
    if not currencies:
        pytest.skip("Нет валют в БД — пропускаем проверку содержимого")

    # Используем поле, которое точно есть в шаблоне (например, char_code)
    first_cur = currencies[0]
    assert first_cur.char_code in html  # ← замени на то, что выводишь в HTML


def test_users_page():
    html = TestServer.make_request('/users')
    users = User.get_all()
    if users:
        assert users[0].name in html


def test_user_page_with_id():
    users = User.get_all()
    if not users:
        pytest.skip("Нет пользователей для теста /user?id=...")

    user = users[0]
    # Получаем подписки
    subs = UserCurrency.get_user_subscriptions(user.id)
    char_codes = [s['char_code'] for s in subs] if subs else []

    html = TestServer.make_request(f'/user?id={user.id}')
    assert user.name in html

    if char_codes:
        expected = ', '.join(char_codes)
        assert expected in html
