# models/database.py

import sqlite3
from models.invoice import Invoice, Item

def init_db():
    conn = sqlite3.connect('invoices.db')
    cursor = conn.cursor()

    # Create invoices table with auto-increment number
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            contact TEXT NOT NULL,
            note TEXT,
            total REAL NOT NULL,
            pay INTEGER CHECK (pay IN (0, 1)) DEFAULT 0
        )
    ''')

    # Create items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number INTEGER,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(invoice_number) REFERENCES invoices(number)
        )
    ''')

    conn.commit()
    conn.close()

def insert_invoice(date, contact, note, total, items):
    conn = sqlite3.connect('invoices.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO invoices (date, contact, note, total)
        VALUES (?, ?, ?, ?)
    ''', (date, contact, note, total))

    invoice_number = cursor.lastrowid

    for item in items:
        cursor.execute('''
            INSERT INTO items (invoice_number, name, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (invoice_number, item.name, item.quantity, item.price))

    conn.commit()
    conn.close()
    return invoice_number

def update_invoice(invoice_number, date, contact, note, total, items):
    conn = sqlite3.connect('invoices.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE invoices
        SET date = ?, contact = ?, note = ?, total = ?
        WHERE number = ?
    ''', (date, contact, note, total, invoice_number))

    # Delete old items
    cursor.execute('DELETE FROM items WHERE invoice_number = ?', (invoice_number,))

    # Insert updated items
    for item in items:
        cursor.execute('''
            INSERT INTO items (invoice_number, name, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (invoice_number, item.name, item.quantity, item.price))

    conn.commit()
    conn.close()

def delete_invoice(invoice_number):
    conn = sqlite3.connect('invoices.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM invoices WHERE number = ?', (invoice_number,))
    cursor.execute('DELETE FROM items WHERE invoice_number = ?', (invoice_number,))

    conn.commit()
    conn.close()

def fetch_invoice(invoice_number):
    conn = sqlite3.connect('invoices.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM invoices WHERE number = ?', (invoice_number,))
    invoice_row = cursor.fetchone()

    if not invoice_row:
        conn.close()
        return None

    invoice = Invoice(number=invoice_row[0], date=invoice_row[1], contact=invoice_row[2], note=invoice_row[3], total=invoice_row[4])

    cursor.execute('SELECT name, quantity, price FROM items WHERE invoice_number = ?', (invoice_number,))
    item_rows = cursor.fetchall()

    items = []
    for item_row in item_rows:
        item = Item(name=item_row[0], quantity=item_row[1], price=item_row[2])
        items.append(item)

    invoice.items = items

    conn.close()
    return invoice

def fetch_invoices_with_filters(filters):
    conn = sqlite3.connect('invoices.db')
    cursor = conn.cursor()

    query = "SELECT * FROM invoices WHERE 1=1"
    params = []

    if "invoice_number" in filters:
        query += " AND number = ?"
        params.append(filters["invoice_number"])

    if "date_from" in filters:
        query += " AND date >= ?"
        params.append(filters["date_from"])

    if "date_to" in filters:
        query += " AND date <= ?"
        params.append(filters["date_to"])

    if "contact" in filters:
        query += " AND contact LIKE ?"
        params.append(f"%{filters['contact']}%")

    if "total_min" in filters:
        query += " AND total >= ?"
        params.append(filters["total_min"])

    if "total_max" in filters:
        query += " AND total <= ?"
        params.append(filters["total_max"])

    if "pay" in filters:
        query += " AND pay = ?"
        params.append(filters["pay"])

    cursor.execute(query, params)
    invoice_rows = cursor.fetchall()

    invoices = []
    for row in invoice_rows:
        invoice = Invoice(number=row[0], date=row[1], contact=row[2], note=row[3], total=row[4], pay=row[5])
        invoices.append(invoice)

    conn.close()
    return invoices
