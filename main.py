import json
from pathlib import Path

PROGRAM_DIRECTORY = Path(__file__).parent
JSON_PATH = PROGRAM_DIRECTORY / "data.json"

if not JSON_PATH.exists():
    with open(JSON_PATH, "w") as file:
        json.dump([], file, indent=4)

with open(JSON_PATH, "r", encoding="utf-8") as file:
    transactions = json.load(file)

def calculate_balance(transactions):
    allowance = sum(
        item["amount"] for item in transactions
        if item["type"] == "allowance"
    )
    expenses = sum(
        item["amount"] for item in transactions
        if item["type"] == "expense"
    )
    return allowance - expenses

with open(JSON_PATH, "w", encoding="utf-8") as file:
    json.dump(transactions, file, indent=4)
    











