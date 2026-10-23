# Personal Finance & Expense Tracker

A Python command-line application for managing personal income and expenses, calculating financial summaries, and
persisting transaction data in JSON format.

## Features

- Add income and expense transactions.
- View all recorded transactions.
- Remove transactions using their UUID.
- Calculate total income, total expenses, and current balance.
- Persist transaction data between application runs using JSON.
- Validate transaction data using Python models and types.
- Run automated tests using `pytest`.

## Installation

### Prerequisites

- Python 3.13 or later
- Git

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Abdelhameed81/personal-finance-tracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd personal-finance-tracker
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment.

   **Windows PowerShell:**

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   source .venv/bin/activate
   ```

## Running the Application

Run the application from the project root:

```bash
python main.py
```

The application provides a menu to add transactions, view transactions, remove transactions, display a financial
summary, and exit.

### Available Operations

1. Add transaction
2. View all transactions
3. Remove transaction
4. View financial summary
5. Exit

Transaction data is stored in a JSON file under the project's `data` directory.

## Running Tests

This project uses `pytest` for automated testing.

1. Install pytest:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Run the test suite from the project root:

   ```bash
   python -m pytest
   ```

The test suite covers the transaction model, ledger, JSON repository, reporting, service layer, CLI, and integration
workflows.

## Project Architecture

The application uses a layered structure to separate business logic, data persistence, reporting, and user interaction.

- **Models** — represent transactions and manage the transaction ledger.
- **Services** — coordinate transaction operations and business logic.
- **Repositories** — handle loading and saving transaction data in JSON format.
- **Reporting** — calculates total income, total expenses, and the current balance.
- **CLI** — provides the interactive command-line interface.
- **Tests** — verify the behaviour of individual components and application workflows.

This structure improves maintainability, supports independent testing, and makes the application easier to extend.