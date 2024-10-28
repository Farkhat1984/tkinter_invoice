# models/invoice.py

class Invoice:
    def __init__(self, number=None, date='', contact='', note='', total=0.0, items=None, pay= 0):
        self.number = number
        self.date = date
        self.contact = contact
        self.note = note
        self.total = total
        self.items = items if items else []
        self.pay = pay

class Item:
    def __init__(self, name='', quantity=0.0, price=0.0):
        self.name = name
        self.quantity = quantity
        self.price = price
