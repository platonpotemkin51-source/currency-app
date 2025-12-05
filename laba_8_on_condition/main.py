from jinja2 import Environment, PackageLoader, select_autoescape
from models import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from utils.currencies_api import *
current_user = None


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global current_user

        if self.path == '/':
            flag = True
            currencies_count = len(Currency.get_all())
            users_count = len(User.get_all())
            author = Author("Platon Potemkin","P3122")
            app = App("First", "1.0.0", author)

            template = env.get_template("index.html")
            result = template.render(
                flag=flag,
                app=app,
                currencies_count=currencies_count,
                users_count=users_count,
            )


        elif self.path == '/author':
            flag = False
            currencies_count = len(Currency.get_all())
            users_count = len(User.get_all())
            author = Author("Platon Potemkin", "P3122")
            app = App("First", "1.0.0", author)

            template = env.get_template("index.html")
            result = template.render(
                app=app,
                currencies_count=currencies_count,
                users_count=users_count,
            )

        elif self.path == '/currencies':
            currencies= Currency.get_all()
            currencies_count = len(Currency.get_all())
            template = env.get_template("currencies.html")
            result = template.render(
                currencies=currencies,
                currencies_count=currencies_count
            )
        elif self.path == '/users':
            users = User.get_all()
            users_count = len(users)
            template = env.get_template("users.html")
            result = template.render(
                users=users,
                users_count=users_count
            )

        for i in User.get_all():
            if self.path == f'/user?id={i.id}':
                user=User.find_by_id(i.id)
                k=[]
                currencies = UserCurrency.get_user_subscriptions(i.id)
                for j in currencies:
                    k.append(j['char_code'])
                sub = ', '.join(k)
                template = env.get_template("user.html")
                result = template.render(
                    sub=sub,
                    user=user,
                    currencies=currencies
            )


        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))
    #
    # def do_POST(self):
    #     global current_user
    #
    #     if self.path == '/register':
    #         content_length = int(self.headers['Content-Length'])
    #         post_data = self.rfile.read(content_length)
    #         data = urllib.parse.parse_qs(post_data.decode('utf-8'))
    #
    #         email = data.get('email', [''])[0]
    #         password = data.get('password', [''])[0]
    #         name = data.get('name', [''])[0]
    #
    #         if User.user_exists(email):
    #             template = env.get_template("register.html")
    #             result = template.render(error="Пользователь с таким email уже существует")
    #         else:
    #             new_user = User.create_user(name, email, password)
    #             current_user = {
    #                 'id': new_user.id,
    #                 'name': new_user.name,
    #                 'email': new_user.email
    #             }
    #             print(f"Успешная регистрация и авторизация: {email}")
    #
    #             self.send_response(302)
    #             self.send_header('Location', '/')
    #             self.end_headers()
    #             return
    #
    #     elif self.path == '/login':
    #         content_length = int(self.headers['Content-Length'])
    #         post_data = self.rfile.read(content_length)
    #         data = urllib.parse.parse_qs(post_data.decode('utf-8'))
    #
    #         email = data.get('email', [''])[0]
    #         password = data.get('password', [''])[0]
    #
    #         user = User.authenticate(email, password)
    #
    #         if user:
    #             current_user = {
    #                 'id': user.id,
    #                 'name': user.name,
    #                 'email': user.email
    #             }
    #             print(f"Успешный вход: {email}")
    #
    #             self.send_response(302)
    #             self.send_header('Location', '/')
    #             self.end_headers()
    #             return
    #         else:
    #             template = env.get_template("login.html")
    #             result = template.render(error="Неверный email или пароль")
    #
    #     self.send_response(200)
    #     self.send_header('Content-Type', 'text/html; charset=utf-8')
    #     self.end_headers()
    #     self.wfile.write(bytes(result, "utf-8"))
    #

env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)


# В самом конце main.py
if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    httpd.serve_forever()

