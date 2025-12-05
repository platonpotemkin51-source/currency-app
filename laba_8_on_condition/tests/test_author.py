import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Author, App


class TestAuthorExtended(unittest.TestCase):
    """Расширенное тестирование класса Author"""

    def test_author_creation_with_default_group(self):
        """Проверка создания объекта Author с группой по умолчанию"""
        author = Author("Потёмкин Платон")
        self.assertEqual(author.name, "Потёмкин Платон")
        self.assertEqual(author.group, "P3122")  # Группа по умолчанию

    def test_author_name_setter_with_whitespace(self):
        """Проверка сеттера имени с пробелами в начале и конце"""
        author = Author("Потёмкин Платон", "P3122")
        author.name = "   Петр Петров   "
        self.assertEqual(author.name, "   Петр Петров   ")  # Сеттер не обрезает пробелы

    def test_author_group_setter_with_5_chars(self):
        """Проверка сеттера группы с ровно 5 символами"""
        author = Author("Потёмкин Платон", "P3122")
        author.group = "P3123"
        self.assertEqual(author.group, "P3123")

    def test_author_group_setter_with_4_chars(self):
        """Проверка сеттера группы с 4 символами (должно вызвать ошибку, так как нужно ровно 5 символов)"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.group = "P312"  # 4 символа
        self.assertIn("Группа должна быть строкой и менее 5 символов", str(context.exception))

    def test_author_group_setter_with_6_chars(self):
        """Проверка сеттера группы с 6 символами (должно вызвать ошибку)"""
        author = Author("Потёмкин Платон", "P3122")
        with self.assertRaises(ValueError) as context:
            author.group = "P31222"  # 6 символов
        self.assertIn("Группа должна быть строкой и менее 5 символов", str(context.exception))

    def test_author_group_setter_with_numeric_chars(self):
        """Проверка сеттера группы с числовыми символами"""
        author = Author("Потёмкин Платон", "P3122")
        author.group = "12345"
        self.assertEqual(author.group, "12345")

    def test_author_group_setter_with_special_chars(self):
        """Проверка сеттера группы со специальными символами"""
        author = Author("Потёмкин Платон", "P3122")
        author.group = "P3-22"
        self.assertEqual(author.group, "P3-22")

    def test_author_name_getter(self):
        """Проверка геттера имени"""
        author = Author("Потёмкин Платон", "P3122")
        self.assertEqual(author.name, "Потёмкин Платон")

    def test_author_group_getter(self):
        """Проверка геттера группы"""
        author = Author("Потёмкин Платон", "P3122")
        self.assertEqual(author.group, "P3122")

    def test_author_private_attributes(self):
        """Проверка, что атрибуты действительно приватные"""
        author = Author("Потёмкин Платон", "P3122")
        
        # Прямой доступ к приватным атрибутам должен быть затруднен
        # Проверим, что обычные атрибуты не существуют
        with self.assertRaises(AttributeError):
            _ = author.__name  # Прямой доступ к приватному атрибуту
        
        with self.assertRaises(AttributeError):
            _ = author.__group  # Прямой доступ к приватному атрибуту
        
        # Но доступ через свойства должен работать
        self.assertEqual(author.name, "Потёмкин Платон")
        self.assertEqual(author.group, "P3122")


class TestAppExtended(unittest.TestCase):
    """Расширенное тестирование класса App"""

    def test_app_version_setter_valid_formats(self):
        """Проверка сеттера версии с различными валидными форматами"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        valid_versions = ["1.0.0", "2.1.5", "10.20.30", "1.0.0.0", "0.0.1"]
        
        for version in valid_versions:
            with self.subTest(version=version):
                app.version = version
                self.assertEqual(app.version, version)

    def test_app_version_setter_invalid_formats(self):
        """Проверка сеттера версии с невалидными форматами"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        invalid_versions = ["1.0.a", "a.b.c", "1..3", ""]
        
        for version in invalid_versions:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    app.version = version

    def test_app_version_setter_non_string(self):
        """Проверка сеттера версии с нестроковыми значениями"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        with self.assertRaises(ValueError) as context:
            app.version = 1.0
        self.assertIn("Версия должна быть строкой", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            app.version = None
        self.assertIn("Версия должна быть строкой", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            app.version = []
        self.assertIn("Версия должна быть строкой", str(context.exception))

    def test_app_author_setter_with_correct_type(self):
        """Проверка сеттера автора с корректным типом"""
        author1 = Author("Потёмкин Платон", "P3122")
        author2 = Author("Иван Иванов", "P3123")
        app = App("Test App", "1.0.0", author1)
        
        app.author = author2
        self.assertEqual(app.author, author2)

    def test_app_author_setter_with_incorrect_type(self):
        """Проверка сеттера автора с некорректным типом"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        with self.assertRaises(ValueError) as context:
            app.author = "Not an Author object"
        self.assertIn("Автор должен быть объектом класса Author", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            app.author = 123
        self.assertIn("Автор должен быть объектом класса Author", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            app.author = None
        self.assertIn("Автор должен быть объектом класса Author", str(context.exception))

    def test_app_name_setter_with_whitespace(self):
        """Проверка сеттера названия приложения с пробелами"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        app.name = "   New App Name   "
        self.assertEqual(app.name, "New App Name")  # Пробелы должны быть обрезаны

    def test_app_name_setter_with_special_chars(self):
        """Проверка сеттера названия приложения со специальными символами"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        special_names = ["App-Name", "App_Name", "App.Name", "App&Name", "App@Name"]
        
        for name in special_names:
            with self.subTest(name=name):
                app.name = name
                self.assertEqual(app.name, name)

    def test_app_creation_with_empty_name_then_set(self):
        """Проверка создания приложения с именем, а затем установка пустого имени"""
        author = Author("Потёмкин Платон", "P3122")
        app = App("Test App", "1.0.0", author)
        
        with self.assertRaises(ValueError) as context:
            app.name = ""
        self.assertIn("Название приложения должно быть строкой не менее 1 символа", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            app.name = " "
        self.assertIn("Название приложения должно быть строкой не менее 1 символа", str(context.exception))


if __name__ == '__main__':
    unittest.main()