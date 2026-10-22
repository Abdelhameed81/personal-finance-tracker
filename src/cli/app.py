from datetime import datetime
from decimal import Decimal, InvalidOperation

from src.models.transaction import TransactionType, IncomeCategory, ExpenseCategory, Transaction
from src.services.transaction_service import TransactionService


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


def ask_for_transaction_category(transaction_type: TransactionType) -> IncomeCategory | ExpenseCategory:
    categories = (
        list(IncomeCategory)
        if transaction_type is TransactionType.INCOME
        else list(ExpenseCategory)
    )
    displayed_options = "\n".join(
        f"{i}. {category.name}"
        for i, category in enumerate(categories, start=1)
    )
    user_message = ("Please select one of the following options:\n" + displayed_options + "\n> ")
    while True:
        user_input = input(user_message).strip()
        try:
            user_choice = int(user_input)
            if 1 <= user_choice <= len(categories):
                return categories[user_choice - 1]
            print(
                f"Invalid choice. Please enter a number between "
                f"1 and {len(categories)}."
            )
            continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue


def ask_for_transaction_amount() -> Decimal:
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


def ask_for_transaction_description() -> str:
    user_message = "Please add description for your transaction: "
    while True:
        user_input = input(user_message).strip()
        if not user_input:
            user_message = "Description can't be empty, please try again: "
            continue
        return user_input


def add_transaction(transaction_service: TransactionService) -> None:
    transaction_type = ask_for_transaction_type()
    new_transaction = Transaction(
        date=datetime.now(),
        type=transaction_type,
        amount=ask_for_transaction_amount(),
        category=ask_for_transaction_category(transaction_type),
        description=ask_for_transaction_description(),
    )
    transaction_service.add_transaction(new_transaction)


def run_app(transaction_service: TransactionService) -> None:
    while True:
        show_menu()
        selection = input("Please select an option ... ")
        match selection:
            case "1":
                add_transaction(transaction_service)
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
        break
