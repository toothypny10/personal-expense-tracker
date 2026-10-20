import json
from pathlib import Path

PROGRAM_DIRECTORY = Path(__file__).parent
JSON_PATH = PROGRAM_DIRECTORY / "data.json"

def load_transaction(): # goes into save_transaction(here) and calculate_balance(here)
    if not JSON_PATH.exists():
        save_transaction([])
        return []

    with open(JSON_PATH, "r", encoding="utf-8") as file:
        transactions = json.load(file)
        if not isinstance(transactions, list):
            raise ValueError("data.json must contain list of transaction.")

        if not transactions:
            return transactions

        ids_added = False
        required_fields = {"type", "amount", "description", "date"}

        for number, transaction in enumerate(transactions, start=1):
            if not isinstance(transaction, dict):
                raise ValueError(f"Transaction {number} must be a dictionary.")

            if not required_fields.issubset(transaction):
                error_id = transaction.get("id", number)
                raise ValueError(f"Transaction {error_id} is missing required fields.")

            if "id" not in transaction or transaction.get("id") != number:
                transaction["id"] = number
                ids_added = True
    
        if ids_added:
            save_transaction(transactions)

        return transactions

def save_transaction(transactions): # load_transaction() either gives [] or transactions
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)

def calculate_balance(transactions): # load_transaction() either gives [] or transactions
    allowance = sum(
        item["amount"] for item in transactions
        if item["type"].lower() == "allowance"
    )
    expenses = sum(
        item["amount"] for item in transactions
        if item["type"].lower() == "expense"
    )
    
    return allowance - expenses


    











