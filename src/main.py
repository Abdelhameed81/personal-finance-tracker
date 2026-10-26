import sys
from pathlib import Path

from src.cli.app import run_app
from src.repositories.json_transaction_repository import JsonTransactionRepository
from src.services.transaction_service import TransactionService

DATA_FILE = Path(__file__).resolve().parent / "data" / "transactions.json"


def main() -> int:
    repository = JsonTransactionRepository(DATA_FILE)
    try:
        transaction_service = TransactionService(repository)
    except OSError as error:
        print(f"Could not read {DATA_FILE}: {error}", file=sys.stderr)
        return 1
    except (ValueError, KeyError, TypeError) as error:
        # JSONDecodeError is a ValueError; KeyError/TypeError/ValueError also come
        # from bad transaction data (missing fields, wrong categories, bad UUIDs...).
        print(f"The data file {DATA_FILE} is corrupt or invalid:", file=sys.stderr)
        print(f"  {type(error).__name__}: {error}", file=sys.stderr)
        print("The file has not been modified. Fix it or move it aside, then restart.",
              file=sys.stderr)
        return 1

    try:
        run_app(transaction_service)
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted. Your transactions are saved. Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
