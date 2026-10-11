import json
from pathlib import Path

PROGRAM_DIRECTORY = Path(__file__).parent
JSON_PATH = PROGRAM_DIRECTORY / "data.json"

if not JSON_PATH.exists():
    with open(JSON_PATH, "w") as file:
        json.dump([], file, indent=4)

with open(JSON_PATH, "r", encoding="utf-8") as file:
    transactions = json.load(file)

total_allowance = 0
total_expense = 0

transaction_type = input("Type: ").lower().strip()
amount = int(input("Amount: "))
description = input("Description: ")
date = input("Date [yyyy-mm-dd]: ")

new_transactions = {
    "type": transaction_type,
    "amount": amount,
    "description": description,
    "date": date
}

transactions.append(new_transactions)

with open(JSON_PATH, "w", encoding="utf-8") as file:
    json.dump(transactions, file, indent=4)

for transaction in transactions:
    if transaction["type"] == "allowance":
        total_allowance += transaction["amount"]

    if transaction["type"] == "expense":
            total_expense += transaction["amount"]

current_balance = total_allowance - total_expense

print(f"Current Balance: ₱{current_balance}")










