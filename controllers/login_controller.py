# controllers/login_controller.py

from views.main_view import MainView

USERNAME = "admin"
PASSWORD = "admin"

class LoginController:
    def __init__(self, view):
        self.view = view

    def check_login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        if username == USERNAME and password == PASSWORD:
            self.view.destroy()
            main_view = MainView()
            main_view.run()
        else:
            self.view.show_error("Неверный логин или пароль")
