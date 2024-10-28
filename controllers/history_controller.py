# controllers/history_controller.py

from models.database import fetch_invoices_with_filters, delete_invoice
from models.invoice import Invoice
from datetime import datetime
from tkinter import ttk, messagebox
from views.invoice_view import InvoiceView

class HistoryController:
    def __init__(self, view):
        self.view = view
        self.current_sort_column = None
        self.current_sort_order = 'asc'

    def update_history_display(self):
        filters = self.view.get_filters()
        invoices = fetch_invoices_with_filters(filters)

        # Sorting
        if self.current_sort_column:
            reverse = True if self.current_sort_order == 'desc' else False
            col_indices = {
                'invoice_number': lambda inv: int(inv.number),
                'date': lambda inv: datetime.strptime(inv.date, '%Y-%m-%d'),
                'contact': lambda inv: inv.contact.lower(),
                'total': lambda inv: float(inv.total),
            }
            key_func = col_indices[self.current_sort_column]
            invoices.sort(key=key_func, reverse=reverse)

        # Передача данных в представление для обновления Treeview
        self.view.update_history_tree(invoices)

    def sort_by_column(self, column_name):
        if self.current_sort_column == column_name:
            self.current_sort_order = 'desc' if self.current_sort_order == 'asc' else 'asc'
        else:
            self.current_sort_column = column_name
            self.current_sort_order = 'asc'
        self.update_history_display()

    def delete_invoice_entry(self, invoice_number):
        confirm = messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить накладную {invoice_number}?")
        if confirm:
            delete_invoice(invoice_number)
            self.update_history_display()

    def open_existing_invoice(self, invoice_number):
        invoice_view = InvoiceView(self.view.parent, invoice_number=invoice_number)
        invoice_view.run()
        # After editing, refresh the history display
        self.update_history_display()
