import json
from pathlib import Path

PROGRAM_DIRECTORY = Path(__file__).parent
JSON_PATH = PROGRAM_DIRECTORY / "data.json"

def load_transaction(): # goes into save_transaction(here) and calculate_balance(here)
    if not JSON_PATH.exists():
        return []

    with open(JSON_PATH, "r", encoding="utf-8") as file:
        transactions = json.load(file)
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


    











