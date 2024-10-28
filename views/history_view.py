import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.history_controller import HistoryController

class HistoryView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = HistoryController(self)

        # Создание нового окна для отображения истории накладных
        self.history_window = tk.Toplevel(self.parent)
        self.history_window.title("История накладных")
        self.history_window.geometry("1200x900")
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)
        # Создание фрейма для фильтров
        filter_frame = ttk.Frame(self.history_window)
        filter_frame.pack(fill='x', padx=10, pady=5)

        # Создание и размещение полей для фильтрации
        ttk.Label(filter_frame, text="Номер:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.invoice_number_var = tk.StringVar()
        invoice_number_entry = ttk.Entry(filter_frame, textvariable=self.invoice_number_var, width=10)
        invoice_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(filter_frame, text="Дата с:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.date_from_var = tk.StringVar()
        date_from_entry = DateEntry(filter_frame, textvariable=self.date_from_var, width=12, date_pattern='yyyy-mm-dd')
        date_from_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(filter_frame, text="по:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.date_to_var = tk.StringVar()
        date_to_entry = DateEntry(filter_frame, textvariable=self.date_to_var, width=12, date_pattern='yyyy-mm-dd')
        date_to_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(filter_frame, text="Контакт:").grid(row=0, column=6, padx=5, pady=5, sticky='w')
        self.contact_var = tk.StringVar()
        contact_entry = ttk.Entry(filter_frame, textvariable=self.contact_var, width=15)
        contact_entry.grid(row=0, column=7, padx=5, pady=5, sticky='w')

        ttk.Label(filter_frame, text="Сумма от:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.total_min_var = tk.StringVar()
        total_min_entry = ttk.Entry(filter_frame, textvariable=self.total_min_var, width=10)
        total_min_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(filter_frame, text="до:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.total_max_var = tk.StringVar()
        total_max_entry = ttk.Entry(filter_frame, textvariable=self.total_max_var, width=10)
        total_max_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(filter_frame, text="Статус оплаты:").grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.pay_status_var = tk.IntVar()  # 0: Все, 1: Оплачено, 2: Неоплачено

        # Радиокнопки для выбора статуса оплаты
        all_radio = ttk.Radiobutton(filter_frame, text="Все", variable=self.pay_status_var, value=0)
        paid_radio = ttk.Radiobutton(filter_frame, text="Оплачено", variable=self.pay_status_var, value=1)
        unpaid_radio = ttk.Radiobutton(filter_frame, text="Неоплачено", variable=self.pay_status_var, value=2)

        all_radio.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        paid_radio.grid(row=1, column=6, padx=5, pady=5, sticky='w')
        unpaid_radio.grid(row=1, column=7, padx=5, pady=5, sticky='w')

        # Кнопка для выполнения поиска с применением фильтров
        search_button = ttk.Button(filter_frame, text="Поиск", command=self.controller.update_history_display)
        search_button.grid(row=1, column=8, padx=5, pady=5, sticky='e')

        # Создание фрейма для отображения истории накладных
        self.history_frame = ttk.Frame(self.history_window)
        self.history_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Определение колонок для отображения истории накладных
        self.history_columns = ["invoice_number", "date", "contact", "total", "edit", "delete"]

        # Создание Treeview для отображения истории накладных
        self.history_tree = ttk.Treeview(self.history_frame, columns=self.history_columns, show='headings')
        self.history_tree.pack(side='left', fill='both', expand=True)

        # Настройка заголовков колонок
        self.history_tree.heading("invoice_number", text="Номер", command=lambda: self.sort_by("invoice_number"))
        self.history_tree.heading("date", text="Дата", command=lambda: self.sort_by("date"))
        self.history_tree.heading("contact", text="Контакт", command=lambda: self.sort_by("contact"))
        self.history_tree.heading("total", text="Сумма", command=lambda: self.sort_by("total"))
        self.history_tree.heading("edit", text="Редактировать")
        self.history_tree.heading("delete", text="Удалить")

        # Настройка ширины и выравнивания колонок
        self.history_tree.column("invoice_number", width=100)
        self.history_tree.column("date", width=100)
        self.history_tree.column("contact", width=200)
        self.history_tree.column("total", width=100, anchor='e')
        self.history_tree.column("edit", width=100, anchor='center')
        self.history_tree.column("delete", width=100, anchor='center')

        # Добавление полос прокрутки
        scrollbar_y = ttk.Scrollbar(self.history_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side='right', fill='y')

        scrollbar_x = ttk.Scrollbar(self.history_window, orient='horizontal', command=self.history_tree.xview)
        self.history_tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(fill='x')

        # Привязка обработчика событий для кликов по Treeview
        self.history_tree.bind('<ButtonRelease-1>', self.on_treeview_click)

        # Инициализация отображения истории накладных
        self.controller.update_history_display()

    def get_filters(self):
        """
        Сбор данных из фильтров для выполнения поиска.
        Возвращает словарь с применяемыми фильтрами.
        """
        filters = {}
        invoice_number_input = self.invoice_number_var.get().strip()
        if invoice_number_input:
            filters["invoice_number"] = invoice_number_input

        date_from_input = self.date_from_var.get().strip()
        if date_from_input:
            filters["date_from"] = date_from_input

        date_to_input = self.date_to_var.get().strip()
        if date_to_input:
            filters["date_to"] = date_to_input

        contact_input = self.contact_var.get().strip()
        if contact_input:
            filters["contact"] = contact_input

        total_min_input = self.total_min_var.get().strip()
        if total_min_input:
            filters["total_min"] = total_min_input

        total_max_input = self.total_max_var.get().strip()
        if total_max_input:
            filters["total_max"] = total_max_input

        # Добавление фильтра по статусу оплаты
        pay_status_input = self.pay_status_var.get()
        if pay_status_input == 1:
            filters["pay"] = 1  # Только оплаченные
        elif pay_status_input == 2:
            filters["pay"] = 0  # Только неоплаченные

        return filters

    def update_history_tree(self, invoices):
        """
        Обновляет Treeview с данными накладных.
        """
        # Очистка текущего содержимого Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Заполнение Treeview данными
        for index, invoice in enumerate(invoices):
            values = (
                invoice.number,
                invoice.date,
                invoice.contact,
                "{:.2f}".format(invoice.total),
                'Редактировать',
                'Удалить'
            )
            self.history_tree.insert('', 'end', values=values)

    def on_treeview_click(self, event):
        """
        Обработка кликов по элементам Treeview.
        """
        item_id = self.history_tree.identify_row(event.y)
        column = self.history_tree.identify_column(event.x)
        if item_id:
            # Получение данных о выбранном элементе
            item = self.history_tree.item(item_id)
            values = item['values']
            # Определение номера колонки
            col_num = int(column.replace('#', '')) - 1
            invoice_number = values[0]
            if col_num == 4:  # Колонка "Редактировать"
                self.edit_invoice(invoice_number)
            elif col_num == 5:  # Колонка "Удалить"
                self.delete_invoice(invoice_number)

    def edit_invoice(self, invoice_number):
        """
        Открывает выбранную накладную для редактирования.
        """
        self.controller.open_existing_invoice(invoice_number)

    def delete_invoice(self, invoice_number):
        """
        Удаляет выбранную накладную после подтверждения.
        """
        self.controller.delete_invoice_entry(invoice_number)

    def sort_by(self, column_name):
        """
        Сортирует данные в Treeview по указанной колонке.
        """
        self.controller.sort_by_column(column_name)

    def run(self):
        """
        Запуск основного цикла окна истории накладных.
        """
        self.history_window.mainloop()
