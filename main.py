import sys
allowance_expense_option = input("Add allowance or expense [a/e]: ").lower()

allowance = 0
expense = 0

if allowance_expense_option == "a": #Allowance
    amount_recieved = int(input("Amount recieved: "))
    # source = input("Source: ")
    # date = input("Date [yyyy-mm-dd]: ")

    allowance += amount_recieved

elif allowance_expense_option == "e": #Expense
    amount_spent = int(input("Amount spent: "))
    # category = input("Category: ")
    # description = input("Lunch")
    # date = input("Date [yyyy-mm-dd]: ")

    expense += amount_spent

else:
    print("You chose none the option!")
    
current_balance = allowance - expense
print(f"Current_balance: {current_balance}")


