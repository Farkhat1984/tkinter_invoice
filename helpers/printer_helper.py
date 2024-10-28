import os
from tkinter import messagebox, Tk, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def print_invoice(invoice_number, date, contact, note, total, items):
    try:
        # Регистрация шрифта DejaVuSans, который поддерживает кириллицу
        font_name = 'DejaVuSans'
        font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
        if not os.path.exists(font_path):
            messagebox.showerror("Ошибка", "Файл шрифта DejaVuSans.ttf не найден.")
            return
        pdfmetrics.registerFont(TTFont(font_name, font_path))

        # Открытие диалогового окна для выбора пути сохранения
        root = Tk()
        root.withdraw()  # Скрыть главное окно Tkinter
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Сохранить накладную как"
        )
        root.destroy()

        if not save_path:
            # Пользователь отменил сохранение
            return

        # Настройка PDF
        c = canvas.Canvas(save_path, pagesize=A4)
        width, height = A4

        # Начальная позиция для текста
        y_position = height - 50
        line_height = 14  # Междустрочный интервал

        # Установка шрифта
        c.setFont(font_name, 12)

        # Заголовок
        c.setFont(font_name, 14)
        c.drawString(50, y_position, f"Накладная №: {invoice_number or 'Новая'}")
        y_position -= line_height * 2
        c.setFont(font_name, 12)
        c.drawString(50, y_position, f"Дата: {date}")
        y_position -= line_height
        c.drawString(50, y_position, f"Контакт: {contact}")
        y_position -= line_height * 2

        # Заголовки таблицы
        c.setFont(font_name, 12)
        c.drawString(50, y_position, "Наименование")
        c.drawString(250, y_position, "Кол-во")
        c.drawString(350, y_position, "Цена")
        c.drawString(450, y_position, "Сумма")
        y_position -= line_height
        c.line(50, y_position, 550, y_position)  # Разделительная линия
        y_position -= line_height

        # Товары
        c.setFont(font_name, 10)
        for item in items:
            name = item.name
            quantity = item.quantity
            price = item.price
            item_sum = float(quantity) * float(price)
            c.drawString(50, y_position, name)
            c.drawString(250, y_position, str(quantity))
            c.drawString(350, y_position, f"{float(price):.2f}")
            c.drawString(450, y_position, f"{item_sum:.2f}")
            y_position -= line_height
            if y_position < 50:
                c.showPage()
                y_position = height - 50
                c.setFont(font_name, 10)

        # Итоговая сумма
        y_position -= line_height
        c.setFont(font_name, 12)
        c.drawString(50, y_position, f"Итого: {total}")
        y_position -= line_height * 2

        # Примечание
        c.setFont(font_name, 10)
        c.drawString(50, y_position, f"Примечание: {note}")
        y_position -= line_height * 2

        # Подпись
        c.drawString(50, y_position, "Спасибо за ваш заказ!")

        # Сохранение PDF
        c.save()

        messagebox.showinfo("Успех", f"Накладная успешно сохранена по пути:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Ошибка печати", f"Не удалось создать PDF-файл: {e}")
