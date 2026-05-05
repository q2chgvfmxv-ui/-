import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.api import convert
from app.storage import load_history, save_history


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.history = load_history()
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY"]

        self.build_ui()
        self.update_table()

    def build_ui(self):
        self.from_cur = ttk.Combobox(self.root, values=self.currencies)
        self.from_cur.set("USD")
        self.from_cur.pack()

        self.to_cur = ttk.Combobox(self.root, values=self.currencies)
        self.to_cur.set("EUR")
        self.to_cur.pack()

        self.amount = tk.Entry(self.root)
        self.amount.pack()

        tk.Button(self.root, text="Convert", command=self.convert).pack()

        self.result = tk.Label(self.root, text="")
        self.result.pack()

        self.table = ttk.Treeview(self.root, columns=("time","from","to","amount","result"), show="headings")
        for c in self.table["columns"]:
            self.table.heading(c, text=c)
        self.table.pack()

    def convert(self):
        try:
            amount = float(self.amount.get())
            if amount <= 0:
                raise ValueError

            result = convert(amount, self.from_cur.get(), self.to_cur.get())

            self.result.config(text=str(result))

            record = {
                "time": str(datetime.now())[:19],
                "from": self.from_cur.get(),
                "to": self.to_cur.get(),
                "amount": amount,
                "result": round(result, 2)
            }

            self.history.append(record)
            save_history(self.history)
            self.update_table()

        except:
            messagebox.showerror("Error", "Invalid input")

    def update_table(self):
        for i in self.table.get_children():
            self.table.delete(i)

        for h in self.history[-20:]:
            self.table.insert("", "end", values=(
                h["time"], h["from"], h["to"], h["amount"], h["result"]
            ))
