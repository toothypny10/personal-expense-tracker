import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import math
from main import load_transaction, save_transaction, calculate_balance, calculate_allowance, calculate_expenses

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Personal Expense Tracker")
        self.geometry("1200x750")
        self.resizable(True, True)
        self.configure(fg_color="#F3F6F4")
        self.transactions = load_transaction()

        self.create_heading()
        self.create_summary_row()
        self.create_dashboard_panels()
        self.refresh_history_table()
        
    def create_heading(self):
        heading = ctk.CTkLabel(
            self,
            text="A little clarity for your money.",
            font=("Nunito Sans", 20, "bold"),
            text_color="#23352D",
        )
        heading_p = ctk.CTkLabel(
            self,
            text="Your allowance, everyday expenses, and everything in between.",
            font=("Nunito Sans", 11),
            text_color="#23352D",
        )
        heading.pack(anchor="w", padx=24, pady=(28,0))
        heading_p.pack(anchor="w", padx=24)

    def create_summary_row(self):
        summary_row = ctk.CTkFrame(self, fg_color="transparent")
        summary_row.pack(fill="x", padx=24, pady=12)
        summary_row.grid_columnconfigure((0, 1, 2), weight=1)

        #card
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
        
        #title
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

        #label
        self.balance_label = ctk.CTkLabel(
            balance_card,
            text=f"\u20b1{calculate_balance(self.transactions):.2f}",
            font=("Arial", 22),
            text_color="#FFFFFF",
        )
        self.allowance_label = ctk.CTkLabel(
            allowance_card,
            text=f"\u20b1{calculate_allowance(self.transactions):.2f}",
            font=("Arial", 22),
            text_color="#23352D",
        )
        self.expenses_label = ctk.CTkLabel(
            expenses_card,
            text=f"\u20b1{calculate_expenses(self.transactions):.2f}",
            font=("Arial", 22),
            text_color="#23352D",
        )

        #packing up
        balance_title.pack(anchor="w", padx=20, pady=(16, 0))
        allowance_title.pack(anchor="w", padx=20, pady=(16, 0))
        expenses_title.pack(anchor="w", padx=20, pady=(16, 0))

        balance_card.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        allowance_card.grid(row=0, column=1, sticky="ew", padx=6)
        expenses_card.grid(row=0, column=2, sticky="ew", padx=(6, 0))

        self.balance_label.pack(anchor="w", padx=20, pady=(4, 16))
        self.allowance_label.pack(anchor="w", padx=20, pady=(4, 16))
        self.expenses_label.pack(anchor="w", padx=20, pady=(4, 16))

    def create_dashboard_panels(self):
        dashboard = ctk.CTkFrame(self, fg_color="transparent")
        dashboard.pack(fill="both", expand=True, padx=24, pady=12)

        dashboard.grid_columnconfigure(0, weight=7, uniform="panels")
        dashboard.grid_columnconfigure(1, weight=3, uniform="panels")
        dashboard.grid_rowconfigure(0, weight=1)

        history_panel = ctk.CTkFrame(
            dashboard,
            fg_color="#FFFFFF",
            corner_radius=12,
        )
        transaction_panel = ctk.CTkFrame(
            dashboard,
            fg_color="#FFFFFF",
            corner_radius=12,
        )

        history_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        transaction_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.build_transaction_panel(transaction_panel)
        self.build_transaction_history(history_panel)

    def build_transaction_panel(self, transaction_panel):
        transaction_title = ctk.CTkLabel(
        transaction_panel,
        text="New transaction",
        font=("Arial", 18, "bold"),
        text_color="#23352D",
        )
        transaction_title.pack(anchor="w", padx=35, pady=(20, 4))

        form = ctk.CTkFrame(                                            # Form Tab
            transaction_panel,
            fg_color="#FFFFFF",
            corner_radius=12,
        )
        form.grid_columnconfigure(0, weight=1)
        form.pack(fill="x", padx=20, pady=16)

        self.type_var = tk.StringVar(value="Allowance")                      # Type Entry

        type_selector = ctk.CTkSegmentedButton(
            form,
            values=["Allowance", "Expense"],
            variable=self.type_var,
            fg_color="#F3F6F4",
            selected_color="#FFFFFF",
            selected_hover_color="#E8EEEA",
            unselected_color="#F3F6F4",
            unselected_hover_color="#E8EEEA",
            text_color="#66736C",
            font=("Arial", 11),
            height=32,
            )
        type_selector.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=12,
            pady=10,
        )
        # Entry
        ctk.CTkLabel(                                                         # Amount Entry
            form, text="Amount:",
            anchor="w",
            font=("Arial", 13),
            text_color="#23352D",
        ).grid(row=1, column=0, sticky="ew", padx=12, pady=(10, 0))

        self.amount_entry = ctk.CTkEntry(
            form, 
            font=("Arial", 11), 
            placeholder_text="\u20b10.00",
            )
        self.amount_entry.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 10))

        ctk.CTkLabel(                                                          # Description Entry
            form, text="Description:",
            anchor="w",
            font=("Arial", 13),
            text_color="#23352D",
        ).grid(row=3, column=0, sticky="ew", padx=12, pady=(10, 0))

        self.description_entry = ctk.CTkEntry(
            form,
            font=("Arial", 11),
            placeholder_text="What was it for?",
        )
        self.description_entry.grid(row=4, column=0, sticky="ew", padx=12, pady=(4, 10))

        ctk.CTkLabel(                                                           # Date Entry
            form, text="Date (YYYY-MM-DD):", 
            anchor="w",
            font=("Arial", 13),
            text_color="#23352D",
        ).grid(row=5, column=0, sticky="ew", padx=12, pady=(10, 0))

        self.date_entry = ctk.CTkEntry(
            form,
            font=("Arial", 11),
            placeholder_text="YYYY-MM-DD",
        )
        self.date_entry.grid(row=6, column=0, sticky="ew", padx=12, pady=(4, 10))
        self.date_entry.insert(0, date.today().isoformat())

        add_button = ctk.CTkButton(
            form,
            text="Add transaction",
            command=self.collect_transaction,
            font=("Arial", 11, "bold"),
            fg_color="#287A55",
            hover_color="#1F6344",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
        )
        add_button.grid(row=7, column=0, sticky="ew",padx=12, pady=(16, 4))

        self.status_label = ctk.CTkLabel(
            form,
            text="",
            font=("Arial", 10),
            text_color="#23352D",
        )
        self.status_label.grid(row=8, column=0, sticky="ew", pady=(4, 0))

    def build_transaction_history(self, history_panel):
        history_title = ctk.CTkLabel(
        history_panel,
        text="Transaction history",
        font=("Arial", 18, "bold"),
        text_color="#23352D",
        )
        history_title.pack(anchor="w", padx=35, pady=(20, 4))

        history_frame = tk.Frame(history_panel, bg="#FFFFFF")
        history_frame.pack(padx=20, pady=20, fill="both", expand=True)

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

        self.history_table = ttk.Treeview(
            history_frame,
            columns=("date", "type", "description", "amount"),
            show="headings",
            height=8,
            style="Expense.Treeview",
        )

        self.history_table.heading("date", text="Date")
        self.history_table.heading("type", text="Type")
        self.history_table.heading("description", text="Description")
        self.history_table.heading("amount", text="Amount")

        self.history_table.column("date", width=110)
        self.history_table.column("type", width=100)
        self.history_table.column("description", width=350)
        self.history_table.column("amount", width=120, anchor="e")

        history_scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_table.yview,
        )

        self.history_table.configure(yscrollcommand=history_scrollbar.set)

        self.history_table.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")

    def collect_transaction(self):
        amount_text = self.amount_entry.get().strip()
        try:
            amount = float(amount_text)
            if not math.isfinite(amount) or amount <= 0:
                raise ValueError
        except ValueError:
            self.status_label.configure(
                text="Enter a finite amount greater than zero.", 
                text_color="#B42318"
            )
            return
    
        date_text = self.date_entry.get().strip()
        try:
            transaction_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    
        except ValueError:
            self.status_label.configure(
                text="Enter a valid date in YYYY-MM-DD format.",
                text_color="#B42318"
            )
            return
    
        
    
        existing_id = [item["id"] for item in self.transactions]
        next_id = max(existing_id, default=0) + 1
        
        transaction = {
            "type": self.type_var.get(),
            "amount": amount,
            "description": self.description_entry.get().strip(),
            "date": transaction_date.isoformat(),
            "id": next_id,
        }
    
        self.transactions.append(transaction)
        save_transaction(self.transactions)
        self.refresh_history_table()
    
        self.status_label.configure(
            text="Transaction added.", 
            text_color="#287A55"
        )
    
        total_balance = calculate_balance(self.transactions)
        total_allowance = calculate_allowance(self.transactions)
        total_expenses = calculate_expenses(self.transactions)
    
        self.balance_label.configure(
            text=f"\u20b1{total_balance:.2f}"
        )
        self.allowance_label.configure(
            text=f"\u20b1{total_allowance:.2f}"
        )
        self.expenses_label.configure(
            text=f"\u20b1{total_expenses:.2f}"
        )
    
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def refresh_history_table(self):
        for row_id in self.history_table.get_children():
            self.history_table.delete(row_id)
        
        for transaction in self.transactions:
            self.history_table.insert(
                "",
                tk.END,
                values=(
                    transaction["date"],
                    transaction["type"],
                    transaction["description"],
                    f"\u20b1{transaction['amount']:.2f}",
                ),
            )

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()