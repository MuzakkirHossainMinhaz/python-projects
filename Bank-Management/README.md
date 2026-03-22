# Bank Management

A small command-line bank management system in Python. Create accounts, deposit, withdraw, transfer funds, list accounts, and persist data between runs with JSON storage.

## Features

- Create user accounts (name, age, NID, initial deposit)
- View account details (ID, name, balance)
- Deposit and withdraw with simple validation
- Transfer between accounts
- Delete accounts
- List all accounts
- JSON persistence (`bank_data.json`)

## Requirements

- Python 3.8+

## Usage

1. Open terminal and go to the project folder:
   ```bash
   cd d:\python-projects\Bank-Management
   ```
2. Run:
   ```bash
   python main.py
   ```
3. Choose menu options:
   - `1` create account
   - `2` view account
   - `3` deposit
   - `4` withdraw
   - `5` transfer
   - `6` list accounts
   - `7` delete account
   - `0` exit

## Project Structure

- `main.py`: BankAccount class, Bank management class, and CLI menu
- `README.md`: Project information and usage
- `bank_data.json`: Auto-generated persisted account data

## Data persistence

Account data is saved automatically when changes are made and loaded on startup. If `bank_data.json` is missing, a new data file is initialized automatically.

## Notes

- Input is validated for integer and float conversion
- Withdrawals and transfers enforce sufficient balance
- Account IDs are auto-incremented
