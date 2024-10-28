import tkinter as tk
from tkinter import ttk
from controllers.login_controller import LoginController

class LoginView:
    def __init__(self):
        self.controller = LoginController(self)
        self.root = tk.Tk()
        self.root.title("Вход")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Создание заголовка
        title_label = ttk.Label(
            self.main_frame,
            text="Авторизация"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Метка и поле ввода для логина
        username_label = ttk.Label(
            self.main_frame,
            text="Логин:"
        )
        username_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)

        self.username_entry = ttk.Entry(self.main_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Метка и поле ввода для пароля
        password_label = ttk.Label(
            self.main_frame,
            text="Пароль:"
        )
        password_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)

        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Метка для сообщений об ошибках
        self.error_label = ttk.Label(
            self.main_frame,
            text=""
        )
        self.error_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

        # Кнопка входа
        self.login_button = ttk.Button(
            self.main_frame,
            text="Войти",
            command=self.controller.check_login
        )
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10)

    def run(self):
        self.root.mainloop()

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def show_error(self, message):
        self.error_label.config(text=message)

    def destroy(self):
        self.root.destroy()
