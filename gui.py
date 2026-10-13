import tkinter as tk
from tkinter import ttk
from datetime import datetime
from main import load_transaction, save_transaction, calculate_balance


def collect_transaction():
    amount_text = amount_entry.get().strip()
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        status_label.config(
            text="Please enter an amount greater than zero.", 
            fg="#B42318"
        )
        return

    date_text = date_entry.get().strip()
    
    try:
        transaction_date = datetime.strptime(date_text, "%Y-%m-%d").date()

    except ValueError:
        status_label.config(
            text="Enter a valid date in YYYY-MM-DD format.",
            fg="#B42318"
        )
        return
    
    transaction = {
        "type": type_var.get(),
        "amount": amount,
        "description": description_entry.get().strip(),
        "date": transaction_date.isoformat()
    }

    transactions = load_transaction()
    transactions.append(transaction)
    save_transaction(transactions)
    refresh_history_table()

    status_label.config(
        text="Transaction added.", 
        fg="#287A55"
    )

    balance = calculate_balance(transactions)
    balance_label.config(text=f"Current Balance: \u20b1{balance:.2f}")

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    type_var.set("Expense")

def refresh_history_table():
    for row_id in history_table.get_children():
        history_table.delete(row_id)

    for transaction in load_transaction():
        history_table.insert(
            "",
            tk.END,
            values=(
                transaction["date"],
                transaction["type"],
                transaction["description"],
                f"\u20b1{transaction['amount']:.2f}",
            ),
        )

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1000x750")
root.resizable(False, False)
root.configure(bg="#F3F6F4")

transactions = load_transaction()


heading = tk.Label(
    root,
    text="EXpnse",
    font=("Arial", 18, "bold"),
    bg="#F3F6F4",
    fg="#23352D",
)
heading.pack(pady=(28, 12))

balance_label = tk.Label(
    root,
    text=f"Current Balance: \u20b1{calculate_balance(transactions):.2f}",
    font=("Arial", 16, "bold"),
    bg="#F3F6F4",
    fg="#287A55",
)
balance_label.pack(pady=12)

form = tk.Frame(root, bg="#FFFFFF", padx=24, pady=20)
form.pack(pady=16)

tk.Label(
    form, text="Type:", font=("Arial", 11),
    bg="#FFFFFF", fg="#23352D",
).grid(row=0, column=0, sticky="w", padx=8, pady=8)

type_var = tk.StringVar(value="Expense")

type_menu = tk.OptionMenu(form, type_var, "Allowance", "Expense")
type_menu.grid(row=0, column=1, padx=8, pady=8)

tk.Label(
    form, text="Amount:", font=("Arial", 11),
    bg="#FFFFFF", fg="#23352D",
).grid(row=1, column=0, sticky="w", padx=8, pady=8)

amount_entry = tk.Entry(form, font=("Arial", 11), width=28)
amount_entry.grid(row=1, column=1, padx=8, pady=8)

tk.Label(
    form, text="Description:", font=("Arial", 11),
    bg="#FFFFFF", fg="#23352D",
).grid(row=2, column=0, sticky="w", padx=8, pady=8)

description_entry = tk.Entry(form, font=("Arial", 11), width=28)
description_entry.grid(row=2, column=1, padx=8, pady=8)

tk.Label(
    form, text="Date (YYYY-MM-DD):", font=("Arial", 11),
    bg="#FFFFFF", fg="#23352D",
).grid(row=3, column=0, sticky="w", padx=8, pady=8)

date_entry = tk.Entry(form, font=("Arial", 11), width=28)
date_entry.grid(row=3, column=1, padx=8, pady=8)

add_button = tk.Button(
    form,
    text="Add transaction",
    command=collect_transaction,
    font=("Arial", 11, "bold"),
    bg="#287A55",
    fg="#FFFFFF",
    activebackground="#1F6344",
    activeforeground="#FFFFFF",
    relief="flat",
    padx=14,
    pady=7,
    cursor="hand2",
)
add_button.grid(row=4, column=0, columnspan=2, pady=(16, 4))

status_label = tk.Label(
    form,
    text="",
    font=("Arial", 10),
    bg="#FFFFFF",
)
status_label.grid(row=5, column=0, columnspan=2, pady=(4, 0))

# Transaction History 
history_table = ttk.Treeview(
    root,
    columns=("date", "type", "description", "amount"),
    show="headings",
    height=8,
)

history_table.heading("date", text="Date")
history_table.heading("type", text="Type")
history_table.heading("description", text="Description")
history_table.heading("amount", text="Amount")

history_table.column("date", width=110)
history_table.column("type", width=100)
history_table.column("description", width=350)
history_table.column("amount", width=120, anchor="e")

history_table.pack(padx=24, pady=12, fill="x")

refresh_history_table()
root.mainloop()
