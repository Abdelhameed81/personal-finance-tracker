from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

from src.models.transaction import TransactionType, IncomeCategory, ExpenseCategory, Transaction
from src.services.transaction_reporter import TransactionReporter
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


def view_all_transactions(transaction_service: TransactionService) -> None:
    transactions = transaction_service.transactions
    if not transactions:
        print("There are no transactions")
    else:
        print("==========================START=================================")
        for transaction in transactions:
            print(f"Transaction: {transaction.uuid}")
            print(f"Date: {transaction.date}")
            print(f"Type: {transaction.type.name}")
            print(f"Amount: £{transaction.amount}")
            print(f"Category: {transaction.category.name}")
            print(f"Description: {transaction.description}")
            print("============================================================\n")
        print("=========================END====================================")


def remove_transaction(transaction_service: TransactionService) -> None:
    view_all_transactions(transaction_service)
    transactions = transaction_service.transactions
    if not transactions:
        return
    try:
        transaction_uuid = UUID(input("Please enter a transaction uuid: ").strip())
    except ValueError:
        print("Invalid uuid, please enter a valid uuid.")
        return
    transaction_to_remove = transaction_service.get_transaction_by_uuid(transaction_uuid)
    if transaction_to_remove is None:
        print("No transaction not found with that UUID")
        return
    transaction_service.remove_transaction(transaction_to_remove)
    print("Transaction removed successfully")


def view_financial_summary(transaction_service: TransactionService) -> None:
    transactions = transaction_service.transactions
    reporter = TransactionReporter(transactions)
    print("========== Financial Summary ==========")
    print(f"{"Total Income:":<20} £{reporter.total_income()}")
    print(f"{"Total Expenses:":<20} £{reporter.total_expenses()}")
    print(f"{"Balance:":<20} £{reporter.balance}")
    print("=======================================")


def run_app(transaction_service: TransactionService) -> None:
    while True:
        show_menu()
        selection = input("Please select an option ... ")
        match selection:
            case "1":
                add_transaction(transaction_service)
            case "2":
                view_all_transactions(transaction_service)
            case "3":
                remove_transaction(transaction_service)
            case "4":
                view_financial_summary(transaction_service)
            case "5":
                print("Exiting now, thanks and good bye!")
                break
            case _:
                print("Invalid input, please select one of these options")
