# controllers/invoice_controller.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.database import insert_invoice, update_invoice, fetch_invoice
from models.invoice import Item
from helpers.printer_helper import print_invoice
import traceback

class InvoiceController:
    def __init__(self, view):
        self.view = view
        self.table_rows = []

    def calculate_sum(self, event=None):
        total_sum = 0
        for idx, row in enumerate(self.table_rows, start=1):
            try:
                quantity_entry = row["quantity"]
                price_entry = row["price"]

                quantity_str = quantity_entry.get().replace(",", ".")
                price_str = price_entry.get().replace(",", ".")

                # Проверка на плейсхолдеры и пустые значения
                if quantity_entry.cget('foreground') == 'grey' or not quantity_str:
                    quantity = 0.0
                else:
                    quantity = round(float(quantity_str), 2)

                if price_entry.cget('foreground') == 'grey' or not price_str:
                    price = 0.0
                else:
                    price = round(float(price_str), 2)

                row_sum = round(quantity * price, 2)
                row["sum"].config(text=f"{row_sum:.2f}")
                total_sum += row_sum
                row["order"].config(text=str(idx))
            except ValueError:
                row["sum"].config(text="0.00")
                continue
        self.view.total_label.config(text=f"Итого: {total_sum:.2f}")

    def add_row(self, item_data=None):
        row_number = len(self.table_rows) + 1

        order_label = ttk.Label(self.view.table_frame, text=str(row_number))
        order_label.grid(row=row_number, column=0, padx=5, pady=5, sticky='nsew')

        name_var = tk.StringVar()
        name_entry = ttk.Entry(self.view.table_frame, textvariable=name_var)
        name_entry.grid(row=row_number, column=1, padx=5, pady=5, sticky='nsew')

        # Функциональность автозаполнения для названий товаров
        # (Вставьте код для автозаполнения здесь)

        quantity_entry = ttk.Entry(self.view.table_frame)
        quantity_entry.grid(row=row_number, column=2, padx=5, pady=5, sticky='nsew')
        quantity_entry.bind("<KeyRelease>", self.calculate_sum)

        price_entry = ttk.Entry(self.view.table_frame)
        price_entry.grid(row=row_number, column=3, padx=5, pady=5, sticky='nsew')
        price_entry.bind("<KeyRelease>", self.calculate_sum)

        sum_label = ttk.Label(self.view.table_frame, text="0.00")
        sum_label.grid(row=row_number, column=4, padx=5, pady=5, sticky='nsew')

        # Функции для управления плейсхолдерами
        def set_placeholder(entry, placeholder):
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

        def clear_placeholder(event, placeholder):
            entry = event.widget
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black')

        def restore_placeholder(event, placeholder):
            entry = event.widget
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground='grey')

        # Если предоставлены данные товара, заполняем поля
        if item_data:
            name_var.set(item_data.name)
            quantity_entry.insert(0, str(item_data.quantity))
            quantity_entry.config(foreground='black')
            price_entry.insert(0, str(item_data.price))
            price_entry.config(foreground='black')
            self.view.item_names.add(item_data.name)
        else:
            # Устанавливаем плейсхолдеры для новых строк
            set_placeholder(quantity_entry, "0")
            quantity_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "0"))
            quantity_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "0"))

            set_placeholder(price_entry, "0.00")
            price_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, "0.00"))
            price_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, "0.00"))

        # Добавление строки в список table_rows
        self.table_rows.append({
            "order": order_label,
            "name": name_var,
            "name_entry": name_entry,
            "quantity": quantity_entry,
            "price": price_entry,
            "sum": sum_label
        })

        self.view.canvas.update_idletasks()
        self.view.canvas.configure(scrollregion=self.view.canvas.bbox("all"))

    def delete_row(self):
        if self.table_rows:
            last_row = self.table_rows.pop()
            last_row["order"].destroy()
            last_row["name_entry"].destroy()
            last_row["quantity"].destroy()
            last_row["price"].destroy()
            last_row["sum"].destroy()
            self.calculate_sum()
            self.view.canvas.update_idletasks()
            self.view.canvas.configure(scrollregion=self.view.canvas.bbox("all"))

    def save_invoice(self):
        data = self.view.get_invoice_data()
        inv_date = data['date']
        inv_contact = data['contact']
        inv_note = data['note']
        inv_total = data['total']

        if inv_contact:
            items = []
            for row in self.table_rows:
                item_name = row["name"].get()
                quantity_entry = row["quantity"]
                price_entry = row["price"]
                quantity_str = quantity_entry.get()
                price_str = price_entry.get()

                # Пропуск строк с плейсхолдерами или пустыми значениями
                if quantity_entry.cget('foreground') == 'grey' or not quantity_str:
                    continue
                if price_entry.cget('foreground') == 'grey' or not price_str:
                    continue

                if item_name:
                    item = Item(name=item_name, quantity=quantity_str, price=price_str)
                    items.append(item)
                    self.view.item_names.add(item_name)

            if self.view.invoice_number:
                # Обновление существующей накладной
                update_invoice(self.view.invoice_number, inv_date, inv_contact, inv_note, inv_total, items)
                messagebox.showinfo("Сохранение", "Накладная обновлена успешно!")
                self.view.invoice_window.destroy()
            else:
                # Создание новой накладной
                new_invoice_number = insert_invoice(inv_date, inv_contact, inv_note, inv_total, items)
                self.view.invoice_number_var.set(str(new_invoice_number))
                messagebox.showinfo("Сохранение",
                                    f"Накладная сохранена успешно!\nНомер накладной: {new_invoice_number}")
                self.view.invoice_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните контакт.")

    def print_invoice(self):
        try:
            data = self.view.get_invoice_data()
            items = []
            for row in self.table_rows:
                item_name = row["name"].get()
                quantity = row["quantity"].get()
                price = row["price"].get()
                if item_name and quantity and price and quantity != "Количество" and price != "Цена":
                    item = Item(name=item_name, quantity=quantity, price=price)
                    items.append(item)
            print_invoice(self.view.invoice_number, data['date'], data['contact'], data['note'], data['total'], items)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при печати: {e}")
            traceback.print_exc()

    def share_invoice(self):
        messagebox.showinfo("Поделиться", "Функция 'Поделиться' пока не реализована.")

    def load_invoice(self, invoice_number):
        invoice = fetch_invoice(invoice_number)
        if invoice is None:
            messagebox.showerror("Ошибка", f"Накладная с номером {invoice_number} не найдена.")
            self.view.invoice_window.destroy()
            return

        self.view.invoice_number_var.set(str(invoice.number))
        self.view.invoice_date_entry.insert(0, invoice.date)
        self.view.contact_entry.insert(0, invoice.contact)
        note_content = invoice.note if invoice.note else ''
        self.view.note_text.insert('1.0', note_content)

        for item in invoice.items:
            self.add_row(item_data=item)
            self.view.item_names.add(item.name)
        self.calculate_sum()
