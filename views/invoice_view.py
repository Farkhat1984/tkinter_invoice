import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.invoice_controller import InvoiceController

class InvoiceView:
    def __init__(self, parent, invoice_number=None):
        self.parent = parent  # Родительский виджет (обычно главное окно)
        self.invoice_number = invoice_number  # Номер накладной (если редактируется существующая)
        self.controller = InvoiceController(self)  # Контроллер для обработки логики

        # Создание нового окна для накладной
        self.invoice_window = tk.Toplevel(self.parent)
        self.invoice_window.title("Создать накладную" if not invoice_number else f"Редактировать накладную № {invoice_number}")
        self.invoice_window.geometry("1200x900")  # Размер окна

        # Создание полей для накладной

        # Номер накладной
        ttk.Label(self.invoice_window, text="Номер накладной:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.invoice_number_var = tk.StringVar()
        self.invoice_number_entry = ttk.Entry(self.invoice_window, textvariable=self.invoice_number_var, state='readonly')
        self.invoice_number_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Дата накладной
        ttk.Label(self.invoice_window, text="Дата:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.invoice_date_entry = ttk.Entry(self.invoice_window)
        self.invoice_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Контактное лицо или организация
        ttk.Label(self.invoice_window, text="Контакт:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.contact_entry = ttk.Entry(self.invoice_window)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Примечание к накладной
        ttk.Label(self.invoice_window, text="Примечание:").grid(row=3, column=0, padx=10, pady=5, sticky='nw')
        self.note_text = tk.Text(self.invoice_window, height=4, width=50)
        self.note_text.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Статус оплаты (чекбокс)
        self.pay_status_var = tk.IntVar()  # 0 для неоплачено, 1 для оплачено
        self.pay_checkbox = ttk.Checkbutton(self.invoice_window, text="Оплачено", variable=self.pay_status_var)
        self.pay_checkbox.grid(row=8, column=3, padx=10, pady=5, sticky='w')

        # Кнопка сохранения накладной
        self.save_button = ttk.Button(self.invoice_window, text="Сохранить", command=self.controller.save_invoice)
        self.save_button.grid(row=8, column=0, padx=10, pady=10, sticky='w')

        # Кнопка печати накладной
        self.print_button = ttk.Button(self.invoice_window, text="Печать", command=self.controller.print_invoice)
        self.print_button.grid(row=8, column=1, padx=10, pady=10, sticky='w')

        # Кнопка поделиться накладной
        self.share_button = ttk.Button(self.invoice_window, text="Поделиться", command=self.controller.share_invoice)
        self.share_button.grid(row=8, column=2, padx=10, pady=10, sticky='w')

        # Метка для отображения общей суммы
        self.total_label = ttk.Label(self.invoice_window, text="Итого: 0.00")
        self.total_label.grid(row=7, column=0, columnspan=5, padx=10, pady=10, sticky='e')

        # Инициализация набора названий товаров для автозаполнения (если используется)
        self.item_names = set()

        # Инициализация списка строк таблицы накладной
        self.table_rows = []

        # Настройка заголовков и весов столбцов таблицы
        self.headers = ["№", "Наименование", "Количество", "Цена", "Сумма"]
        self.column_weights = [1, 3, 2, 2, 2]

        # Настройка таблицы товаров
        self.setup_table()

        # Кнопка добавления новой строки в таблицу
        self.add_row_button = ttk.Button(self.invoice_window, text="Добавить строку", command=self.controller.add_row)
        self.add_row_button.grid(row=6, column=0, padx=10, pady=5, sticky='w')

        # Кнопка удаления выбранной строки из таблицы
        self.delete_row_button = ttk.Button(self.invoice_window, text="Удалить строку", command=self.controller.delete_row)
        self.delete_row_button.grid(row=6, column=1, padx=10, pady=5, sticky='w')

        # Повторное создание кнопок сохранения, печати и поделиться (возможно, избыточно)
        self.save_button = ttk.Button(self.invoice_window, text="Сохранить", command=self.controller.save_invoice)
        self.save_button.grid(row=8, column=0, padx=10, pady=10, sticky='w')

        self.print_button = ttk.Button(self.invoice_window, text="Печать", command=self.controller.print_invoice)
        self.print_button.grid(row=8, column=1, padx=10, pady=10, sticky='w')

        self.share_button = ttk.Button(self.invoice_window, text="Поделиться", command=self.controller.share_invoice)
        self.share_button.grid(row=8, column=2, padx=10, pady=10, sticky='w')

        # Загрузка существующей накладной или инициализация новой
        if invoice_number:
            self.controller.load_invoice(invoice_number)  # Загрузка данных существующей накладной
        else:
            self.invoice_number_var.set("Будет присвоен автоматически")  # Установка сообщения для нового номера
            self.invoice_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Установка текущей даты
            for _ in range(10):
                self.controller.add_row()  # Добавление 10 пустых строк по умолчанию

    def setup_table(self):
        # Настройка веса строк и столбцов для корректного масштабирования
        self.invoice_window.grid_rowconfigure(5, weight=1)  # Строка с таблицей растягивается
        for col, weight in enumerate(self.column_weights):
            self.invoice_window.grid_columnconfigure(col, weight=weight, uniform='column')

        # Создание заголовка таблицы
        header_frame = ttk.Frame(self.invoice_window)
        header_frame.grid(row=4, column=0, columnspan=5, sticky='ew', padx=10)
        for i, weight in enumerate(self.column_weights):
            header_frame.grid_columnconfigure(i, weight=weight, uniform='column')
        for col_num, header in enumerate(self.headers):
            header_label = ttk.Label(header_frame, text=header)
            header_label.grid(row=0, column=col_num, padx=5, pady=5, sticky='nsew')

        # Создание канваса с полосой прокрутки для таблицы
        self.canvas = tk.Canvas(self.invoice_window)
        self.canvas.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        self.scrollbar = ttk.Scrollbar(self.invoice_window, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=5, column=5, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Создание внутреннего фрейма для размещения строк таблицы внутри канваса
        self.table_frame = ttk.Frame(self.canvas)
        self.table_frame_id = self.canvas.create_window((0, 0), window=self.table_frame, anchor='nw')

        # Привязка события изменения размера канваса к функции обновления ширины table_frame
        self.canvas.bind('<Configure>', self.resize_table_frame)

        for i, weight in enumerate(self.column_weights):
            self.table_frame.grid_columnconfigure(i, weight=weight, uniform='column')

    def resize_table_frame(self, event):
        # Обновление ширины table_frame при изменении размера канваса
        canvas_width = event.width
        self.canvas.itemconfig(self.table_frame_id, width=canvas_width)

        # Привязка события прокрутки мышью к канвасу
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        # Обновление области прокрутки при изменении размера содержимого
        self.table_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def on_mouse_wheel(self, event):
        # Обработка прокрутки колесиком мыши
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def get_invoice_data(self):
        # Сбор данных из всех полей накладной для сохранения
        return {
            "invoice_number": self.invoice_number_var.get(),
            "date": self.invoice_date_entry.get(),
            "contact": self.contact_entry.get(),
            "note": self.note_text.get('1.0', tk.END).strip(),
            "total": self.total_label.cget("text").replace("Итого: ", ""),
            "pay": self.pay_status_var.get()  # 0 для неоплачено, 1 для оплачено
        }

    def run(self):
        # Запуск основного цикла окна накладной
        self.invoice_window.mainloop()
