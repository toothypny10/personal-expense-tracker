import tkinter as tk

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("800x500")

heading = tk.Label(
    root,
    text="Personal Expense Tracker by Leo",
    font=("Arial", 15, "bold")
)
heading.pack(pady=20)

balance_label = tk.Label(
    root,
    text="Current Balance: ₱0.00",
    font=("Arial", 10)
)
balance_label.pack(pady=10)

form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Type: ").grid(
    row=0, column=0
)

type_entry = tk.Entry(form)
type_entry.grid(
    row=0, column=1
)

tk.Label(form, text="Amount: ").grid(
    row=1, column=0
)

amount_entry = tk.Entry(form)
amount_entry.grid(
    row=1, column=1
)


root.mainloop()