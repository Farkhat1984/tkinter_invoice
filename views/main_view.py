import tkinter as tk
from tkinter import ttk
from controllers.main_controller import MainController

class MainView:
    def __init__(self):
        self.controller = MainController(self)  # Инициализация контроллера с передачей текущего представления
        self.root = tk.Tk()  # Создание главного окна приложения
        self.root.title("Главная страница")  # Установка заголовка окна
        self.root.geometry("600x400")  # Установка размера окна
        self.root.resizable(False, False)  # Отключение возможности изменения размера окна

        # Создание основного фрейма с отступами
        self.main_frame = ttk.Frame(self.root, padding=30)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')  # Размещение фрейма по центру окна

        # Создание заголовка внутри основного фрейма
        title_label = ttk.Label(
            self.main_frame,
            text="Главная Страница"  # Текст заголовка
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))  # Размещение заголовка в сетке

        # Создание кнопки "Создать накладную"
        create_button = ttk.Button(
            self.main_frame,
            text="Создать накладную",  # Текст кнопки
            command=self.controller.open_create_invoice  # Функция, вызываемая при нажатии
        )
        create_button.grid(row=1, column=0, padx=20, pady=10, sticky='ew')  # Размещение кнопки в сетке

        # Создание кнопки "История"
        history_button = ttk.Button(
            self.main_frame,
            text="История",  # Текст кнопки
            command=self.controller.open_history  # Функция, вызываемая при нажатии
        )
        history_button.grid(row=2, column=0, padx=20, pady=10, sticky='ew')  # Размещение кнопки в сетке

        # Создание кнопки "Выйти"
        exit_button = ttk.Button(
            self.main_frame,
            text="Выйти",  # Текст кнопки
            command=self.root.destroy  # Функция, вызываемая при нажатии (закрытие приложения)
        )
        exit_button.grid(row=3, column=0, padx=20, pady=10, sticky='ew')  # Размещение кнопки в сетке

    def run(self):
        self.root.mainloop()  # Запуск основного цикла приложения
