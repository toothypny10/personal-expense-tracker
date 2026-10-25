import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from main import load_transaction, save_transaction, calculate_balance, calculate_allowance, calculate_expenses
import math
from datetime import date, datetime

def collect_transaction():
    amount_text = amount_entry.get().strip()
    try:
        amount = float(amount_text)
        if not math.isfinite(amount) or amount <= 0:
            raise ValueError
    except ValueError:
        status_label.configure(
            text="Enter a finite amount greater than zero.", 
            text_color="#B42318"
        )
        return

    date_text = date_entry.get().strip()
    try:
        transaction_date = datetime.strptime(date_text, "%Y-%m-%d").date()

    except ValueError:
        status_label.configure(
            text="Enter a valid date in YYYY-MM-DD format.",
            text_color="#B42318"
        )
        return

    transactions = load_transaction()

    existing_id = [item["id"] for item in transactions]
    next_id = max(existing_id, default=0) + 1
    
    transaction = {
        "type": type_var.get(),
        "amount": amount,
        "description": description_entry.get().strip(),
        "date": transaction_date.isoformat(),
        "id": next_id,
    }

    transactions.append(transaction)
    save_transaction(transactions)
    refresh_history_table()

    status_label.configure(
        text="Transaction added.", 
        text_color="#287A55"
    )

    total_balance = calculate_balance(transactions)
    total_allowance = calculate_allowance(transactions)
    total_expenses = calculate_expenses(transactions)

    balance_label.configure(
        text=f"\u20b1{total_balance:.2f}"
    )
    allowance_label.configure(
        text=f"\u20b1{total_allowance:.2f}"
    )
    expenses_label.configure(
        text=f"\u20b1{total_expenses:.2f}"
    )

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    type_var.set("Allowance")

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

# GUI
root = ctk.CTk()
root.title("Personal Expense Tracker")
root.geometry("1200x750")
root.resizable(True, True)
root.configure(fg_color="#F3F6F4")

transactions = load_transaction()

# Program Name/"Expense" header
heading = ctk.CTkLabel(
    root,
    text="EXpnse",
    font=("Arial", 18, "bold"),
    text_color="#23352D",
)
heading.pack(pady=(28, 12))

#Summary Part j ngato, agitay total t balance, allowance, kn expenses.
summary_row = ctk.CTkFrame(root, fg_color="transparent")
summary_row.pack(fill="x", padx=24, pady=12)
summary_row.grid_columnconfigure((0, 1, 2), weight=1)

balance_card = ctk.CTkFrame(            
    summary_row,
    fg_color="#356B50",
    corner_radius=12,
)
allowance_card = ctk.CTkFrame(
    summary_row, 
    fg_color="#FFFFFF",                             
    corner_radius=12
    )
expenses_card = ctk.CTkFrame(
    summary_row, 
    fg_color="#FFFFFF", 
    corner_radius=12
    )

balance_title = ctk.CTkLabel(
    balance_card,
    text="Available balance",
    font=("Arial", 12),
    text_color="#FFFFFF",
)
allowance_title = ctk.CTkLabel(
    allowance_card,
    text="Total allowance",
    font=("Arial", 12),
    text_color="#23352D",
)
expenses_title = ctk.CTkLabel(
    expenses_card,
    text="Total expenses",
    font=("Arial",12),
    text_color="#23352D",
)

balance_label = ctk.CTkLabel(
    balance_card,
    text=f"\u20b1{calculate_balance(transactions):.2f}",
    font=("Arial", 22),
    text_color="#FFFFFF",
)
allowance_label = ctk.CTkLabel(
    allowance_card,
    text=f"\u20b1{calculate_allowance(transactions):.2f}",
    font=("Arial", 22),
    text_color="#23352D",
)
expenses_label = ctk.CTkLabel(
    expenses_card,
    text=f"\u20b1{calculate_expenses(transactions):.2f}",
    font=("Arial", 22),
    text_color="#23352D",
)

balance_title.pack(anchor="w", padx=20, pady=(16, 0))
allowance_title.pack(anchor="w", padx=20, pady=(16, 0))
expenses_title.pack(anchor="w", padx=20, pady=(16, 0))

balance_card.grid(row=0, column=0, sticky="ew", padx=(0, 6))
allowance_card.grid(row=0, column=1, sticky="ew", padx=6)
expenses_card.grid(row=0, column=2, sticky="ew", padx=(6, 0))

balance_label.pack(anchor="w", padx=20, pady=(4, 16))
allowance_label.pack(anchor="w", padx=20, pady=(4, 16))
expenses_label.pack(anchor="w", padx=20, pady=(4, 16))

# Side-by-side dashboard panels
dashboard = ctk.CTkFrame(root, fg_color="transparent")
dashboard.pack(fill="both", expand=True, padx=24, pady=12)

dashboard.grid_columnconfigure(0, weight=3)
dashboard.grid_columnconfigure(1, weight=2)
dashboard.grid_rowconfigure(0, weight=1)

history_panel = ctk.CTkFrame(
    dashboard,
    fg_color="#FFFFFF",
    corner_radius=12,
)
history_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

transaction_panel = ctk.CTkFrame(
    dashboard,
    fg_color="#FFFFFF",
    corner_radius=12,
)
transaction_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))


# New Transaction Tab
transaction_title = ctk.CTkLabel(
    transaction_panel,
    text="New transaction",
    font=("Arial", 18, "bold"),
    text_color="#23352D",
)
transaction_title.pack(anchor="w", padx=20, pady=(20, 4))

form = ctk.CTkFrame(                                            # Form Tab
    transaction_panel,
    fg_color="#FFFFFF",
    corner_radius=12,
)
form.pack(pady=16)

ctk.CTkLabel(                                                       # Type Entry
    form, text="Type:", font=("Arial", 13),
    text_color="#23352D",
).grid(row=0, column=0, sticky="w", padx=12, pady=10)

type_var = tk.StringVar(value="Allowance")

type_menu = ctk.CTkOptionMenu(
    form, 
    variable=type_var, 
    values=["Allowance", "Expense"],
    )
type_menu.grid(row=0, column=1, padx=12, pady=10)

# Entry
ctk.CTkLabel(                                                         # Amount Entry
    form, text="Amount:", font=("Arial", 13),
    text_color="#23352D",
).grid(row=1, column=0, sticky="w", padx=12, pady=10)

amount_entry = ctk.CTkEntry(
    form, 
    font=("Arial", 11), 
    width=260, 
    placeholder_text="\u20b10.00",
    )
amount_entry.grid(row=1, column=1, padx=12, pady=10)

ctk.CTkLabel(                                                          # Description Entry
    form, text="Description:", font=("Arial", 13),
    text_color="#23352D",
).grid(row=2, column=0, sticky="w", padx=12, pady=10)

description_entry = ctk.CTkEntry(
    form,
    font=("Arial", 11),
    width=260,
    placeholder_text="What was it for?",
)
description_entry.grid(row=2, column=1, padx=12, pady=10)

ctk.CTkLabel(                                                           # Date Entry
    form, text="Date (YYYY-MM-DD):", font=("Arial", 13),
    text_color="#23352D",
).grid(row=3, column=0, sticky="w", padx=12, pady=10)

date_entry = ctk.CTkEntry(
    form,
    font=("Arial", 11),
    width=260,
    placeholder_text="YYYY-MM-DD",
)
date_entry.grid(row=3, column=1, padx=12, pady=10)
date_entry.insert(0, date.today().isoformat())

add_button = ctk.CTkButton(
    form,
    text="Add transaction",
    command=collect_transaction,
    font=("Arial", 11, "bold"),
    fg_color="#287A55",
    hover_color="#1F6344",
    text_color="#FFFFFF",
    width=260,
    height=40,
    corner_radius=8,
)
add_button.grid(row=4, column=0, columnspan=2, pady=(16, 4))

status_label = ctk.CTkLabel(
    form,
    text="",
    font=("Arial", 10),
    text_color="#23352D",
)
status_label.grid(row=5, column=0, columnspan=2, pady=(4, 0))

# Transaction History 
history_title = ctk.CTkLabel(
    history_panel,
    text="Transaction history",
    font=("Arial", 18, "bold"),
    text_color="#23352D",
)
history_title.pack(anchor="w", padx=20, pady=(20, 4))

history_frame = tk.Frame(history_panel, bg="#FFFFFF")
history_frame.pack(padx=12, pady=12, fill="both", expand=True)

table_style = ttk.Style()
table_style.theme_use("clam")
table_style.configure(
    "Expense.Treeview",
    background="#FFFFFF",
    foreground="#23352D",
    fieldbackground="#FFFFFF",
    rowheight=36,
    font=("Arial", 10),
)
table_style.configure(
    "Expense.Treeview.Heading",
    background="#F3F6F4",
    foreground="#23352D",
    font=("Arial", 10, "bold"),
    relief="flat",
)

history_table = ttk.Treeview(
    history_frame,
    columns=("date", "type", "description", "amount"),
    show="headings",
    height=8,
    style="Expense.Treeview",
)

history_table.heading("date", text="Date")
history_table.heading("type", text="Type")
history_table.heading("description", text="Description")
history_table.heading("amount", text="Amount")

history_table.column("date", width=110)
history_table.column("type", width=100)
history_table.column("description", width=350)
history_table.column("amount", width=120, anchor="e")

history_scrollbar = ttk.Scrollbar(
    history_frame,
    orient="vertical",
    command=history_table.yview,
)

history_table.configure(yscrollcommand=history_scrollbar.set)

history_table.pack(side="left", fill="both", expand=True)
history_scrollbar.pack(side="right", fill="y")

refresh_history_table()
root.mainloop()
