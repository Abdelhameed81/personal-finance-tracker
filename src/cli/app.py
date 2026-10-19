from decimal import Decimal, InvalidOperation

from src.models.transaction import TransactionType


def show_menu() -> None:
    print("Personal Finance Tracker.")
    menu_item = ["1. Add a transaction", "2. View all transactions", "3. Remove a transaction",
                 "4. View financial summary",
                 "5. Exit"]
    for item in menu_item:
        print(item)


def ask_for_transaction_type() -> TransactionType:
    while True:
        category = input("Please choose a transaction type, Income or Expense: ")
        match category.upper().strip():
            case "INCOME":
                return TransactionType.INCOME
            case "EXPENSE":
                return TransactionType.EXPENSE
            case _:
                print("Invalid input, please enter either income or expense")


def ask_for_amount() -> Decimal | None:
    user_message = "Please enter the amount you would like to add: "
    while True:
        user_input = input(user_message).strip()
        try:
            amount = Decimal(user_input)
            if amount <= 0:
                user_message = "Invalid input, please enter a positive number: "
                continue
            if amount.as_tuple().exponent < -2:
                user_message = "Please enter a value with two decimal places: "
                continue
            return amount
        except InvalidOperation:
            user_message = "Invalid amount. Please enter a valid number: "
            continue


def ask_for_description() -> str | None:
    user_message = "Please add description for your transaction: "
    while True:
        user_input = input(user_message).strip()
        if not user_input:
            user_message = "Description can't be empty, please try again: "
            continue
        return user_input


def run_app() -> None:
    while True:
        show_menu()
        selection = input("Please select an option ... ")
        match selection:
            case "1":
                print("Add a transaction is not implemented yet")
            case "2":
                print("View all transactions is not implemented yet")
            case "3":
                print("Remove a transaction is not implemented yet")
            case "4":
                print("View financial summary is not implemented yet")
            case "5":
                print("Exiting now, thanks and good bye!")
                break
            case _:
                print("Invalid input, please select one of these options")
