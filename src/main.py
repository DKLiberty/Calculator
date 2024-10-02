import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Функция для получения курса валют
def get_exchange_rates():
    api_key = "b1413fd51e124e848f9e5ccfe509d79d"  # Вставьте ваш API-ключ Open Exchange Rates
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"]
    else:
        messagebox.showerror("Error", "Unable to fetch exchange rates")
        return None

# Функция для обновления списка валют
def update_to_currency_list(event):
    selected_from_currency = from_currency_combobox.get()
    filtered_currencies = [currency for currency in currencies if currency != selected_from_currency]
    to_currency_combobox['values'] = filtered_currencies
    if to_currency_combobox.get() == selected_from_currency:
        to_currency_combobox.set(filtered_currencies[0])

# Функция для конвертации валют
def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combobox.get()
        to_currency = to_currency_combobox.get()

        # Получаем курс выбранных валют
        rates = get_exchange_rates()
        if rates is None:
            return

        from_rate = rates[from_currency]
        to_rate = rates[to_currency]

        # Выполняем конвертацию
        converted_amount = amount * (to_rate / from_rate)

        # Отображаем результат
        result_var.set(f"{amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}".replace(",", " "))
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Проверка, чтобы вводились только числа
def validate_numeric_input(action, value_if_allowed):
    if action == '1':  # Добавляется символ
        if value_if_allowed == "" or value_if_allowed.replace('.', '', 1).isdigit():
            return True
        else:
            return False
    else:
        return True

# Основное окно
root = tk.Tk()
root.title("Converter Calculator")
root.geometry("800x600")
root.configure(bg="#ffffff")  # Белый фон

# Установить окно в полноэкранный режим
root.attributes('-fullscreen', True)

# Установить иконку на калькулятор
root.iconbitmap("./src/calculator.ico")  # Путь к файлу с иконкой

# Паттерн
PRIMARY_COLOR = "#2A9D8F"
ACCENT_COLOR = "#155049"
TEXT_COLOR = "#264653"

# Стилизация интерфейса
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 14), background="#ffffff", foreground=TEXT_COLOR)
style.configure('TButton', font=('Helvetica', 14), background=PRIMARY_COLOR, foreground="white")
style.configure('TCombobox', font=('Helvetica', 12))

# Фрейм для центрального размещения элементов
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Центровка фрейма

# Заголовок
header_label = tk.Label(frame, text="Converter Calculator", font=('Helvetica', 24, 'bold'), bg="#ffffff", fg=TEXT_COLOR)
header_label.pack(pady=10)

# Переменные
result_var = tk.StringVar()

# Метка и поле для ввода суммы
amount_label = ttk.Label(frame, text="Amount:")
amount_label.pack(pady=10)

# Ограничение для ввода только чисел
vcmd = (root.register(validate_numeric_input), '%d', '%P')

amount_var = tk.StringVar()
amount_entry = ttk.Entry(frame, textvariable=amount_var, validate="key", validatecommand=vcmd, font=('Helvetica', 14), width=30)
amount_entry.pack(pady=10)

# Выпадающие списки для выбора валют
currencies = ["USD", "EUR", "GBP", "TRY", "JPY", "RUB", "AUD", "CAD", "CNY", "CHF", "INR"]  # Добавьте больше валют

from_currency_label = ttk.Label(frame, text="From")
from_currency_label.pack(pady=10)

from_currency_combobox = ttk.Combobox(frame, values=currencies, state="readonly", font=('Helvetica', 14))
from_currency_combobox.current(0)
from_currency_combobox.pack(pady=10)

to_currency_label = ttk.Label(frame, text="To")
to_currency_label.pack(pady=10)

to_currency_combobox = ttk.Combobox(frame, values=currencies[1:], state="readonly", font=('Helvetica', 14))
to_currency_combobox.current(1)
to_currency_combobox.pack(pady=10)

# Обновление второго списка валют при выборе первой
from_currency_combobox.bind("<<ComboboxSelected>>", update_to_currency_list)

# Кнопка для выполнения конвертации
convert_button = tk.Button(frame, text="Convert", command=convert_currency, font=('Helvetica', 16), bg=PRIMARY_COLOR, fg="white", activebackground=ACCENT_COLOR, activeforeground="white", relief="flat", padx=20, pady=10)
convert_button.pack(pady=20)

# Метка для отображения результата
result_label = tk.Label(frame, textvariable=result_var, font=("Helvetica", 18, "bold"), bg="#ffffff", fg=TEXT_COLOR)
result_label.pack(pady=20)

# Запуск главного цикла
root.mainloop()
