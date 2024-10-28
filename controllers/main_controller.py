# controllers/main_controller.py

from models.database import init_db
from views.invoice_view import InvoiceView
from views.history_view import HistoryView

class MainController:
    def __init__(self, view):
        self.view = view
        init_db()  # Initialize the database

    def open_create_invoice(self):
        invoice_view = InvoiceView(self.view.root)
        invoice_view.run()

    def open_history(self):
        history_view = HistoryView(self.view.root)
        history_view.run()
